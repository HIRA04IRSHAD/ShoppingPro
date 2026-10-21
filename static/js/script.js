let currentProducts = [];
let isSearchActive = false;
let visibleCount = 8;

window.onload = function() {
    fetchCategoriesOnLanding();
};

// Sends a query to the Flask /search route, or to the in-browser
// Python engine (Pyodide) when the GitHub Pages demo has set one up.
async function runSearch(query) {
    if (window.shopaiQuery) {
        return await window.shopaiQuery(query);
    }

    const response = await fetch('/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query: query})
    });
    return await response.json();
}

async function fetchCategoriesOnLanding() {
    try {
        const data = await runSearch('show categories');

        if (data.status === "success") {
            const chatBox = document.getElementById('chat-box');
            currentProducts = data.products || [];
            isSearchActive = false;
            visibleCount = 8;

            appendAIMessage(data.reply, chatBox);
            applySorting();
        }
    } catch (error) {
        console.error("Error loading landing page:", error);
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const msg = input.value.trim();
    if (!msg) return;

    appendUserMessage(msg, chatBox);
    input.value = '';

    try {
        const data = await runSearch(msg);

        if (data.status === "success") {
            currentProducts = data.products || [];
            isSearchActive = true;
            visibleCount = 8;

            appendAIMessage(data.reply, chatBox);
            document.getElementById('sort-filter').value = 'deal';
            applySorting();
        } else {
            console.error("Search error:", data.message);
            appendAIMessage("Sorry, something went wrong with that search. Please try again.", chatBox);
        }
    } catch (error) {
        console.error("Search error:", error);
        appendAIMessage("Sorry, the search engine is not available right now. Please refresh the page.", chatBox);
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendAIMessage(text, chatBox) {
    const div = document.createElement('div');
    div.className = 'msg ai-msg';
    div.innerHTML = `
        <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="msg-bubble">${text}</div>
    `;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendUserMessage(text, chatBox) {
    const div = document.createElement('div');
    div.className = 'msg user-msg';
    div.innerHTML = `
        <div class="msg-avatar"><i class="fa-solid fa-user"></i></div>
        <div class="msg-bubble"></div>
    `;
    // textContent so typed text is shown as text, never run as HTML
    div.querySelector('.msg-bubble').textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function applySorting() {
    const sortType = document.getElementById('sort-filter').value;
    let sortedProducts = [...currentProducts];

    if (sortType === 'price-low') {
        sortedProducts.sort((a, b) => a.price - b.price);
    } else if (sortType === 'price-high') {
        sortedProducts.sort((a, b) => b.price - a.price);
    } else if (sortType === 'deal') {
        sortedProducts.sort((a, b) => (b.deal_score || 0) - (a.deal_score || 0));
    }

    renderProducts(sortedProducts);
}

function loadMore() {
    visibleCount += 8;
    applySorting();
}

function renderProducts(products) {
    const grid = document.getElementById('product-grid');
    const countLabel = document.getElementById('result-count');

    if (!products || products.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-box-open"></i>
                <p>No products found. Try a different search!</p>
            </div>`;
        countLabel.innerText = "0 Results";
        const oldBtn = document.getElementById('view-more-container');
        if (oldBtn) oldBtn.remove();
        return;
    }

    countLabel.innerText = isSearchActive
        ? `${products.length} Results Found`
        : `Featured Products`;

    const productsToShow = products.slice(0, visibleCount);

    grid.innerHTML = productsToShow.map(p => `
        <div class="product-card">
            <div class="card-top">
                <span class="category-tag">${p.category}</span>
                ${isSearchActive
                    ? `<span class="score-tag">⚡ ${p.deal_score}</span>`
                    : ''}
            </div>

            <div>
                <div class="card-name" title="${p.name}">${p.name}</div>
                <div class="card-meta" style="margin-top:5px">
                    <span class="card-brand">${p.brand}</span>
                    <span class="card-sep">•</span>
                    <span class="card-platform">${p.platform}</span>
                </div>
            </div>

            <div class="card-price-row">
                <span class="card-price">₹${p.price.toLocaleString()}</span>
                <span class="card-original">₹${p.original_price.toLocaleString()}</span>
            </div>

            <div>
                <span class="discount-badge">
                    <i class="fa-solid fa-tag" style="font-size:9px"></i>
                    ${p.discount}% off
                </span>
            </div>

            ${isSearchActive ? `
            <div class="deal-bar-wrap">
                <div class="deal-bar-label">
                    <span>Deal Score</span>
                    <span>${p.deal_score}/100</span>
                </div>
                <div class="deal-bar">
                    <div class="deal-bar-fill" style="width: ${p.deal_score}%"></div>
                </div>
            </div>` : ''}
        </div>
    `).join('');

    // View More button
    let viewMoreContainer = document.getElementById('view-more-container');

    if (visibleCount < products.length) {
        if (!viewMoreContainer) {
            viewMoreContainer = document.createElement('div');
            viewMoreContainer.id = 'view-more-container';
            grid.parentNode.insertBefore(viewMoreContainer, grid.nextSibling);
        }
        viewMoreContainer.innerHTML = `
            <button onclick="loadMore()">
                Load More <i class="fa-solid fa-chevron-down"></i>
                <span style="opacity:0.6;font-weight:400;font-size:11px">(${products.length - visibleCount} remaining)</span>
            </button>`;
    } else {
        if (viewMoreContainer) viewMoreContainer.remove();
    }
}

// Enter key support
document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
