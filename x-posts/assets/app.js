(() => {
  const data = window.XPOSTS_DATA;
  if (!data) {
    return;
  }

  const PAGE_SIZE = 60;
  const searchInput = document.querySelector("#search-input");
  const folderNav = document.querySelector("#folder-nav");
  const folderSummary = document.querySelector("#folder-summary");
  const postsEl = document.querySelector("#posts");
  const visibleCountEl = document.querySelector("#visible-count");
  const folderCountEl = document.querySelector("#folder-count");
  const loadMoreButton = document.querySelector("#load-more");
  const emptyState = document.querySelector("#empty-state");
  const forcedFolderSlug = document.body.dataset.folderSlug || null;

  const folderMap = new Map(data.folders.map((folder) => [folder.slug, folder]));
  const folderSlugByName = new Map(data.folders.map((folder) => [folder.name, folder.slug]));
  const allBookmarks = [...data.bookmarks].sort((left, right) => right.postedAtTimestamp - left.postedAtTimestamp);

  const state = {
    query: "",
    visibleCount: PAGE_SIZE,
  };

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function formatCompact(value) {
    return new Intl.NumberFormat("en-US", {
      notation: "compact",
      maximumFractionDigits: 1,
    }).format(value || 0);
  }

  function formatDate(value) {
    if (!value) {
      return "";
    }
    return new Date(value).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  function cleanDisplayText(value) {
    let text = value || "";
    if (!text) {
      return "";
    }

    text = text.replace(/https:\/\/t\.co\/\S+/gi, " ");

    text = text
      .replace(/[ \t]+\n/g, "\n")
      .replace(/\n{3,}/g, "\n\n")
      .replace(/[ \t]{2,}/g, " ")
      .trim();

    const lines = text
      .split("\n")
      .map((line) => line.trimEnd())
      .filter((line) => !/^(?:[-*•]|\d+[.)])\s*$/.test(line.trim()));

    return lines.join("\n").trim();
  }

  function displayText(bookmark) {
    return cleanDisplayText(bookmark.text || "");
  }

  function getLinkMeta(url) {
    try {
      const parsed = new URL(url);
      const host = parsed.hostname.replace(/^www\./, "");
      const path = (parsed.pathname || "/").replace(/\/+$/, "") || "/";
      const label = host === "x.com" && path.startsWith("/i/article/") ? "Linked article" : host;
      return { url, host, path, label };
    } catch {
      return { url, host: "", path: url, label: "External link" };
    }
  }

  function pickVideoSource(media) {
    const variants = (media.videoVariants || []).filter((variant) => variant.url);
    const capped = variants
      .filter((variant) => (variant.bitrate || 0) <= 950000)
      .sort((left, right) => (right.bitrate || 0) - (left.bitrate || 0));

    if (capped.length) {
      return capped[0].url;
    }

    variants.sort((left, right) => (right.bitrate || 0) - (left.bitrate || 0));
    return variants[0]?.url || "";
  }

  function renderMedia(mediaObjects) {
    if (!mediaObjects?.length) {
      return "";
    }

    const items = mediaObjects
      .slice(0, 4)
      .map((media) => {
        if (media.type === "video") {
          const videoSource = pickVideoSource(media);
          if (!videoSource) {
            return "";
          }
          return `
            <a class="media-item video-card" href="${escapeHtml(videoSource)}" target="_blank" rel="noreferrer">
              <img loading="lazy" src="${escapeHtml(media.url || "")}" alt="${escapeHtml(media.altText || "Video preview image")}">
              <span class="play-badge" aria-hidden="true">▶</span>
            </a>
          `;
        }

        return `
          <figure class="media-item image">
            <img loading="lazy" src="${escapeHtml(media.url || "")}" alt="${escapeHtml(media.altText || "Bookmark media")}">
          </figure>
        `;
      })
      .join("");

    return `<div class="media-grid media-count-${Math.min(mediaObjects.length, 4)}">${items}</div>`;
  }

  function renderLinkCard(url, label = "External link") {
    if (!url) {
      return "";
    }

    const meta = getLinkMeta(url);
    const displayLabel = label || meta.label;
    return `
      <a class="link-card" href="${escapeHtml(meta.url)}" target="_blank" rel="noreferrer">
        <span class="link-card-label">${escapeHtml(displayLabel)}</span>
        <strong class="link-card-path">${escapeHtml(meta.path)}</strong>
      </a>
    `;
  }

  function renderQuotedTweet(quotedTweet) {
    if (!quotedTweet) {
      return "";
    }

    const text = cleanDisplayText(quotedTweet.text || "");
    const media = renderMedia(quotedTweet.mediaObjects);
    const fallbackLink = !text && !quotedTweet.mediaObjects?.length ? renderLinkCard(quotedTweet.url, "Quoted post") : "";

    return `
      <blockquote class="quoted-tweet">
        <p class="quoted-header">
          <strong>${escapeHtml(quotedTweet.authorName || quotedTweet.authorHandle || "Quoted post")}</strong>
          <span>@${escapeHtml(quotedTweet.authorHandle || "unknown")}</span>
        </p>
        ${text ? `<p>${escapeHtml(text)}</p>` : ""}
        ${fallbackLink}
        ${media}
      </blockquote>
    `;
  }

  function renderBookmark(bookmark) {
    const folderSlug = folderSlugByName.get(bookmark.folder);
    const folder = folderMap.get(folderSlug);
    const text = displayText(bookmark);
    const firstLink = (bookmark.links || []).find(Boolean);
    const hasFallbackLinkCard = !text && !(bookmark.mediaObjects?.length) && !bookmark.quotedTweet && firstLink;

    return `
      <article class="post-card">
        <header class="post-header">
          <div class="author">
            <img class="avatar" loading="lazy" src="${escapeHtml(bookmark.authorProfileImageUrl || "")}" alt="">
            <div>
              <p class="author-name">${escapeHtml(bookmark.authorName || "")}</p>
              <p class="author-handle">@${escapeHtml(bookmark.authorHandle || "")}</p>
            </div>
          </div>
          <div class="post-meta">
            <time datetime="${escapeHtml(bookmark.postedAt || "")}">${escapeHtml(formatDate(bookmark.postedAt))}</time>
            <a class="folder-pill" href="${folder ? `${forcedFolderSlug ? "../../" : ""}folders/${folder.slug}/index.html` : "#"}">${escapeHtml(bookmark.folder || "")}</a>
          </div>
        </header>

        <div class="post-body">
          ${text ? `<p class="post-text">${escapeHtml(text)}</p>` : ""}
          ${renderQuotedTweet(bookmark.quotedTweet)}
          ${renderMedia(bookmark.mediaObjects)}
          ${hasFallbackLinkCard ? renderLinkCard(firstLink) : ""}
        </div>

        <footer class="post-footer">
          <a class="source-link" href="${escapeHtml(bookmark.url || "#")}" target="_blank" rel="noreferrer">View on X</a>
        </footer>
      </article>
    `;
  }

  function buildFolderLink(folder) {
    const currentPrefix = forcedFolderSlug ? "../../" : "";
    const href = currentPrefix + "folders/" + folder.slug + "/index.html";
    const active = folder.slug === forcedFolderSlug ? " is-active" : "";
    return `
      <a class="folder-link${active}" href="${href}">
        <span>${escapeHtml(folder.name)}</span>
        <strong>${folder.count}</strong>
      </a>
    `;
  }

  function renderFolderNav() {
    folderNav.innerHTML = data.folders.map(buildFolderLink).join("");
    folderCountEl.textContent = String(data.folders.length);
  }

  function renderFolderSummary(filtered) {
    const activeFolder = forcedFolderSlug ? folderMap.get(forcedFolderSlug) : null;
    const summaryCards = (activeFolder ? [activeFolder] : data.folders)
      .filter((folder) => !state.query || filtered.some((bookmark) => bookmark.folder === folder.name))
      .map((folder) => {
        return `
          <article class="folder-card">
            <p class="folder-card-title">${escapeHtml(folder.name)}</p>
            <p class="folder-card-copy">${escapeHtml(folder.description)}</p>
            <p class="folder-card-count">${folder.count} bookmarks</p>
          </article>
        `;
      })
      .join("");

    folderSummary.innerHTML = summaryCards;
  }

  function filterBookmarks() {
    const query = state.query.trim().toLowerCase();
    return allBookmarks.filter((bookmark) => {
      const folderSlug = folderSlugByName.get(bookmark.folder);
      if (forcedFolderSlug && folderSlug !== forcedFolderSlug) {
        return false;
      }

      if (!query) {
        return true;
      }

      const haystack = [
        bookmark.text,
        bookmark.authorName,
        bookmark.authorHandle,
        bookmark.folder,
        bookmark.quotedTweet?.text,
        bookmark.quotedTweet?.authorHandle,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();

      return haystack.includes(query);
    });
  }

  function render() {
    const filtered = filterBookmarks();
    const visible = filtered.slice(0, state.visibleCount);

    visibleCountEl.textContent = String(filtered.length);
    renderFolderSummary(filtered);
    postsEl.innerHTML = visible.map(renderBookmark).join("");
    emptyState.hidden = filtered.length !== 0;

    if (filtered.length > state.visibleCount) {
      loadMoreButton.hidden = false;
      loadMoreButton.textContent = `Load more (${filtered.length - state.visibleCount} remaining)`;
    } else {
      loadMoreButton.hidden = true;
    }

  }

  renderFolderNav();
  render();

  searchInput?.addEventListener("input", (event) => {
    state.query = event.target.value;
    state.visibleCount = PAGE_SIZE;
    render();
  });

  loadMoreButton?.addEventListener("click", () => {
    state.visibleCount += PAGE_SIZE;
    render();
  });
})();
