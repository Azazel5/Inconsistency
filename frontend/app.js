// Frontend controller for Inconsistency Analyzer dashboard

const API_BASE = ""; // Relative paths as the server hosts both

// Global state
let playlists = [];
let comparisons = {};
let activeTab = "overview";
let selectedPlaylistId = "";

// Chart references to prevent overlap bugs
let categoryChart = null;
let playlistChart = null;
let incentiveChart = null;
let contentTypeChart = null;

// Initialize app on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
    initApp();
});

async function initApp() {
    setupTabNavigation();
    setupFormSubmission();
    setupPlaylistSelect();
    setupDeleteButton();
    
    // Initial fetch of data
    await refreshData();
}

// 1. TAB SWITCHING SYSTEM
function setupTabNavigation() {
    const navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const tabName = btn.getAttribute("data-tab");
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    activeTab = tabName;
    
    // Update active nav button
    document.querySelectorAll(".nav-btn").forEach(btn => {
        if (btn.getAttribute("data-tab") === tabName) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    });
    
    // Update active panel
    document.querySelectorAll(".tab-panel").forEach(panel => {
        if (panel.id === `panel-${tabName}`) {
            panel.classList.add("active");
        } else {
            panel.classList.remove("active");
        }
    });
    
    // Update titles based on tab
    const titleEl = document.getElementById("page-title");
    const subtitleEl = document.getElementById("page-subtitle");
    
    if (tabName === "overview") {
        titleEl.textContent = "Overview Dashboard";
        subtitleEl.textContent = "Comparative insights on YouTube tutorial playlist retention curves.";
        renderOverviewCharts();
    } else if (tabName === "analyzer") {
        titleEl.textContent = "Playlist Analyzer";
        subtitleEl.textContent = "Deep-dive analysis and decay curve-fitting for individual courses.";
        if (selectedPlaylistId) {
            loadPlaylistDetails(selectedPlaylistId);
        } else if (playlists.length > 0) {
            loadPlaylistDetails(playlists[0].metadata.id);
        }
    } else if (tabName === "hypotheses") {
        titleEl.textContent = "Hypothesis Testing";
        subtitleEl.textContent = "Validating incentives, dropoff patterns, and learning motivation theories.";
        renderHypothesisCharts();
    } else if (tabName === "add-playlist") {
        titleEl.textContent = "Import Playlist";
        subtitleEl.textContent = "Add new tutorial series to expand drop-off analysis datasets.";
    }
}

// 2. DATA LOAD & REFRESH
async function refreshData() {
    showLoading(true);
    try {
        // Fetch playlists list
        const resPlaylists = await fetch(`${API_BASE}/api/playlists`);
        if (!resPlaylists.ok) throw new Error("Failed to load playlists list.");
        playlists = await resPlaylists.json();
        
        // Fetch aggregates
        const resComparisons = await fetch(`${API_BASE}/api/comparisons`);
        if (!resComparisons.ok) throw new Error("Failed to load comparisons aggregate data.");
        comparisons = await resComparisons.json();
        
        // Populate select list and KPI metrics
        populatePlaylistDropdown();
        updateKPICards();
        populateOverviewList();
        
        // Render current active tab's charts
        if (activeTab === "overview") {
            renderOverviewCharts();
        } else if (activeTab === "analyzer") {
            const dropdown = document.getElementById("playlist-select");
            if (dropdown.value) loadPlaylistDetails(dropdown.value);
        } else if (activeTab === "hypotheses") {
            renderHypothesisCharts();
        }
        
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        showLoading(false);
    }
}

function updateKPICards() {
    if (playlists.length === 0) return;
    
    document.getElementById("kpi-playlists").textContent = playlists.length;
    
    const avgDrop = playlists.reduce((acc, p) => acc + p.metrics.first_video_dropoff_percentage, 0) / playlists.length;
    document.getElementById("kpi-dropoff").textContent = `${avgDrop.toFixed(1)}%`;
    
    const avgComp = playlists.reduce((acc, p) => acc + p.metrics.overall_retention_percentage, 0) / playlists.length;
    document.getElementById("kpi-completion").textContent = `${avgComp.toFixed(1)}%`;
    
    // Determine most common best fit model
    let powerCount = 0;
    let expCount = 0;
    playlists.forEach(p => {
        if (p.metrics.best_fit_model === "Power Law") powerCount++;
        if (p.metrics.best_fit_model === "Exponential") expCount++;
    });
    
    const modelStr = powerCount >= expCount ? "Power Law" : "Exponential";
    document.getElementById("kpi-fit").textContent = modelStr;
}

function populatePlaylistDropdown() {
    const dropdown = document.getElementById("playlist-select");
    dropdown.innerHTML = "";
    
    playlists.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.metadata.id;
        opt.textContent = `[${p.metadata.category}] ${p.metadata.title}`;
        dropdown.appendChild(opt);
    });
    
    if (playlists.length > 0 && !selectedPlaylistId) {
        selectedPlaylistId = playlists[0].metadata.id;
    }
}

function populateOverviewList() {
    const container = document.getElementById("playlists-summary-list");
    container.innerHTML = "";
    
    playlists.forEach(p => {
        const item = document.createElement("div");
        item.className = "summary-item";
        item.addEventListener("click", () => {
            selectedPlaylistId = p.metadata.id;
            document.getElementById("playlist-select").value = p.metadata.id;
            switchTab("analyzer");
        });
        
        item.innerHTML = `
            <div class="summary-title-wrapper">
                <span class="summary-title" title="${p.metadata.title}">${p.metadata.title}</span>
                <span class="summary-category">${p.metadata.category} (${p.metadata.incentive_group})</span>
            </div>
            <div class="summary-metrics">
                <div class="summary-stat">
                    <span>Dropoff</span>
                    <strong class="text-rose">${p.metrics.first_video_dropoff_percentage.toFixed(0)}%</strong>
                </div>
                <div class="summary-stat">
                    <span>Completion</span>
                    <strong class="text-emerald">${p.metrics.overall_retention_percentage.toFixed(1)}%</strong>
                </div>
                <div class="summary-stat">
                    <span>Best Fit</span>
                    <strong class="text-blue">${p.metrics.best_fit_model === "Power Law" ? "Power" : "Exp"}</strong>
                </div>
            </div>
        `;
        container.appendChild(item);
    });
}

function setupPlaylistSelect() {
    const select = document.getElementById("playlist-select");
    select.addEventListener("change", (e) => {
        selectedPlaylistId = e.target.value;
        loadPlaylistDetails(selectedPlaylistId);
    });
}

// 3. SINGLE PLAYLIST ANALYZER DETAILS
async function loadPlaylistDetails(playlistId) {
    if (!playlistId) return;
    showLoading(true);
    
    try {
        const res = await fetch(`${API_BASE}/api/playlists/${playlistId}`);
        if (!res.ok) throw new Error("Failed to load playlist details.");
        const data = await res.json();
        
        // Populate metadata
        document.getElementById("detail-category").textContent = data.metadata.category;
        document.getElementById("detail-title").textContent = data.metadata.title;
        document.getElementById("detail-channel").textContent = `by ${data.metadata.channel_title}`;
        document.getElementById("detail-description").textContent = data.metadata.description || "No description provided.";
        
        // Populate Stats
        document.getElementById("stat-videos").textContent = data.metrics.total_videos;
        document.getElementById("stat-views").textContent = formatNumber(data.metrics.total_views);
        document.getElementById("stat-dropoff").textContent = `${data.metrics.first_video_dropoff_percentage.toFixed(1)}%`;
        document.getElementById("stat-completion").textContent = `${data.metrics.overall_retention_percentage.toFixed(1)}%`;
        
        const hl = data.metrics.half_life;
        document.getElementById("stat-halflife").textContent = hl === -1 ? "N/A" : `Video ${hl + 1}`;
        
        // R2 Values & bars
        const powR2 = data.fitting.power.r2;
        const expR2 = data.fitting.exponential.r2;
        
        document.getElementById("pow-r2-val").textContent = powR2.toFixed(3);
        document.getElementById("pow-r2-bar").style.width = `${powR2 * 100}%`;
        
        document.getElementById("exp-r2-val").textContent = expR2.toFixed(3);
        document.getElementById("exp-r2-bar").style.width = `${expR2 * 100}%`;
        
        const verdictEl = document.getElementById("fit-summary-verdict");
        if (powR2 > expR2) {
            verdictEl.innerHTML = `<strong>Verdict: Power Law Fit</strong><br>The curve fits a power-law decay ($R^2 = ${powR2.toFixed(3)}$) better than an exponential one. This indicates a very high initial dropoff (tourist cohort) followed by a highly stabilized committed learning cohort.`;
        } else {
            verdictEl.innerHTML = `<strong>Verdict: Exponential Fit</strong><br>The curve fits an exponential decay ($R^2 = ${expR2.toFixed(3)}$) better than a power-law. This reflects a steady, constant percentage dropoff of users at each progressive video.`;
        }
        
        // Render Single Playlist Charts
        renderPlaylistChart(data);
        
        // Build table
        populateVideoTable(data.videos);
        
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        showLoading(false);
    }
}

function populateVideoTable(videos) {
    const tbody = document.querySelector("#video-breakdown-table tbody");
    tbody.innerHTML = "";
    
    videos.forEach(v => {
        const tr = document.createElement("tr");
        
        const durationStr = formatDuration(v.duration_seconds);
        const dropStr = v.position === 0 ? "—" : `${v.local_dropoff_percentage.toFixed(1)}%`;
        
        tr.innerHTML = `
            <td>${v.position + 1}</td>
            <td style="font-weight: 500; text-align: left;">${v.title}</td>
            <td>${formatNumber(v.view_count)}</td>
            <td>${durationStr}</td>
            <td><strong>${v.retention_percentage.toFixed(1)}%</strong></td>
            <td class="${v.position > 0 ? 'text-rose' : ''}">${dropStr}</td>
        `;
        tbody.appendChild(tr);
    });
}

// 4. CHART RENDERING MODULES
function renderOverviewCharts() {
    if (!comparisons.categories) return;
    
    const ctx = document.getElementById("chart-categories-comparison").getContext("2d");
    
    const datasets = [];
    const colors = [
        "rgba(129, 140, 248, 1)", // Indigo
        "rgba(16, 185, 129, 1)",  // Emerald
        "rgba(244, 63, 94, 1)",   // Rose
        "rgba(59, 130, 246, 1)",   // Blue
        "rgba(245, 158, 11, 1)",   // Amber
        "rgba(168, 85, 247, 1)",   // Purple
        "rgba(236, 72, 153, 1)"    // Pink
    ];
    
    let colorIdx = 0;
    let maxLen = 0;
    
    for (const [name, catData] of Object.entries(comparisons.categories)) {
        if (catData.avg_curve.length > maxLen) maxLen = catData.avg_curve.length;
        
        datasets.append = datasets.push({
            label: `${name} (Avg)`,
            data: catData.avg_curve,
            borderColor: colors[colorIdx % colors.length],
            backgroundColor: colors[colorIdx % colors.length].replace("1)", "0.05)"),
            borderWidth: 2,
            tension: 0.25,
            fill: false
        });
        colorIdx++;
    }
    
    const labels = Array.from({length: maxLen}, (_, i) => `Video ${i + 1}`);
    
    if (categoryChart) categoryChart.destroy();
    
    categoryChart = new Chart(ctx, {
        type: "line",
        data: { labels, datasets },
        options: getChartOptions("Retention Rate (%)")
    });
}

function renderPlaylistChart(playlistData) {
    const ctx = document.getElementById("chart-playlist-retention").getContext("2d");
    
    const actualData = playlistData.videos.map(v => v.retention_percentage);
    const expData = playlistData.fitting.exponential.fitted_curve;
    const powData = playlistData.fitting.power.fitted_curve;
    
    const labels = playlistData.videos.map(v => `Video ${v.position + 1}`);
    
    // Create view count gradient fill
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, "rgba(129, 140, 248, 0.3)");
    gradient.addColorStop(1, "rgba(129, 140, 248, 0.0)");
    
    if (playlistChart) playlistChart.destroy();
    
    playlistChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "Actual Retention",
                    data: actualData,
                    borderColor: "rgba(129, 140, 248, 1)",
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.2,
                    pointRadius: 4,
                    pointBackgroundColor: "rgba(129, 140, 248, 1)"
                },
                {
                    label: `Power Law Fit (R²=${playlistData.fitting.power.r2.toFixed(3)})`,
                    data: powData,
                    borderColor: "rgba(16, 185, 129, 0.8)",
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.2,
                    pointRadius: 0
                },
                {
                    label: `Exponential Fit (R²=${playlistData.fitting.exponential.r2.toFixed(3)})`,
                    data: expData,
                    borderColor: "rgba(59, 130, 246, 0.8)",
                    borderWidth: 2,
                    borderDash: [3, 3],
                    fill: false,
                    tension: 0.2,
                    pointRadius: 0
                }
            ]
        },
        options: getChartOptions("Retention Rate (%)")
    });
}

function renderHypothesisCharts() {
    if (!comparisons.incentives) return;
    
    // 1. INCENTIVE COMPARISON CHART
    const ctxInc = document.getElementById("chart-incentives-comparison").getContext("2d");
    
    const datasetInc = [];
    const maxLenInc = Math.max(
        comparisons.incentives.Incentive ? comparisons.incentives.Incentive.avg_curve.length : 0,
        comparisons.incentives.Aspirational ? comparisons.incentives.Aspirational.avg_curve.length : 0
    );
    
    if (comparisons.incentives.Incentive) {
        datasetInc.push({
            label: `Incentives (Jobs/Exams/Certs) [${comparisons.incentives.Incentive.count} Lists]`,
            data: comparisons.incentives.Incentive.avg_curve,
            borderColor: "rgba(129, 140, 248, 1)", // Purple
            backgroundColor: "rgba(129, 140, 248, 0.05)",
            borderWidth: 3,
            tension: 0.2,
            fill: true
        });
    }
    
    if (comparisons.incentives.Aspirational) {
        datasetInc.push({
            label: `Aspirational (Hobby/Self-improvement) [${comparisons.incentives.Aspirational.count} Lists]`,
            data: comparisons.incentives.Aspirational.avg_curve,
            borderColor: "rgba(244, 63, 94, 1)", // Rose
            backgroundColor: "rgba(244, 63, 94, 0.05)",
            borderWidth: 3,
            tension: 0.2,
            fill: true
        });
    }
    
    const labelsInc = Array.from({length: maxLenInc}, (_, i) => `Video ${i + 1}`);
    
    if (incentiveChart) incentiveChart.destroy();
    
    incentiveChart = new Chart(ctxInc, {
        type: "line",
        data: { labels: labelsInc, datasets: datasetInc },
        options: getChartOptions("Retention Rate (%)")
    });
    
    // 2. CONTENT TYPE COMPARISON CHART
    if (!comparisons.content_types) return;
    const ctxType = document.getElementById("chart-content-types-comparison").getContext("2d");
    
    const datasetType = [];
    const colors = [
        "rgba(16, 185, 129, 1)",  // Emerald
        "rgba(59, 130, 246, 1)",   // Blue
        "rgba(245, 158, 11, 1)",   // Amber
        "rgba(168, 85, 247, 1)",   // Purple
        "rgba(129, 140, 248, 1)"   // Indigo
    ];
    
    let maxLenType = 0;
    let colorIdx = 0;
    
    for (const [name, typeData] of Object.entries(comparisons.content_types)) {
        if (typeData.avg_curve.length > maxLenType) maxLenType = typeData.avg_curve.length;
        
        datasetType.push({
            label: `${name} [${typeData.count} Lists]`,
            data: typeData.avg_curve,
            borderColor: colors[colorIdx % colors.length],
            borderWidth: 2,
            tension: 0.25,
            fill: false
        });
        colorIdx++;
    }
    
    const labelsType = Array.from({length: maxLenType}, (_, i) => `Video ${i + 1}`);
    
    if (contentTypeChart) contentTypeChart.destroy();
    
    contentTypeChart = new Chart(ctxType, {
        type: "line",
        data: { labels: labelsType, datasets: datasetType },
        options: getChartOptions("Retention Rate (%)")
    });
}

// Chart.js helper options for dark mode
function getChartOptions(yLabel) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#e5e7eb', // text-secondary
                    font: { family: 'Inter', size: 12 }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(14, 18, 26, 0.95)',
                titleColor: '#f3f4f6',
                bodyColor: '#e5e7eb',
                borderColor: 'rgba(255,255,255,0.1)',
                borderWidth: 1,
                padding: 12,
                boxPadding: 8,
                callbacks: {
                    label: function(context) {
                        return ` ${context.dataset.label}: ${context.raw.toFixed(1)}%`;
                    }
                }
            }
        },
        scales: {
            x: {
                grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                ticks: { color: '#9ca3af', font: { family: 'Inter', size: 10 } }
            },
            y: {
                min: 0,
                max: 100,
                grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                ticks: {
                    color: '#9ca3af',
                    font: { family: 'Inter', size: 10 },
                    callback: function(value) { return value + '%'; }
                },
                title: {
                    display: true,
                    text: yLabel,
                    color: '#9ca3af',
                    font: { family: 'Inter', size: 11 }
                }
            }
        }
    };
}

// 5. IMPORTING PLAYLIST FORM
function setupFormSubmission() {
    const form = document.getElementById("add-playlist-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const url_or_id = document.getElementById("url_or_id").value.strip ? document.getElementById("url_or_id").value.strip() : document.getElementById("url_or_id").value;
        const category = document.getElementById("category").value;
        const expected_retention = document.getElementById("expected_retention").value;
        const incentive_group = document.getElementById("incentive_group").value;
        const content_type = document.getElementById("content_type").value;
        
        // Show loading in form button
        const btnText = document.querySelector("#btn-submit-playlist .btn-text");
        const spinner = document.getElementById("form-spinner");
        
        btnText.textContent = "Fetching Live API Data...";
        spinner.style.display = "inline-block";
        document.getElementById("btn-submit-playlist").disabled = true;
        
        try {
            const res = await fetch(`${API_BASE}/api/playlists/add`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url_or_id,
                    category,
                    expected_retention,
                    incentive_group,
                    content_type
                })
            });
            
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Failed to add playlist.");
            
            showToast("Playlist imported and analyzed successfully!", "success");
            
            // Clean up form
            form.reset();
            
            // Refresh application state
            selectedPlaylistId = data.metadata.id;
            await refreshData();
            
            // Navigate to Analyzer tab for the new playlist
            switchTab("analyzer");
            
        } catch (err) {
            showToast(err.message, "error");
        } finally {
            btnText.textContent = "Fetch & Analyze Playlist";
            spinner.style.display = "none";
            document.getElementById("btn-submit-playlist").disabled = false;
        }
    });
}

// 6. DELETING PLAYLISTS
function setupDeleteButton() {
    const btn = document.getElementById("btn-delete-playlist");
    btn.addEventListener("click", async () => {
        if (!selectedPlaylistId) return;
        
        const confirmDelete = confirm("Are you sure you want to delete this playlist from the database?");
        if (!confirmDelete) return;
        
        showLoading(true);
        try {
            const res = await fetch(`${API_BASE}/api/playlists/delete/${selectedPlaylistId}`, {
                method: "POST"
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Failed to delete playlist.");
            
            showToast("Playlist deleted successfully.", "success");
            selectedPlaylistId = ""; // Reset selection
            
            await refreshData();
            switchTab("overview"); // Back to overview
            
        } catch (err) {
            showToast(err.message, "error");
        } finally {
            showLoading(false);
        }
    });
}

// 7. INTERFACING UTILS
function showLoading(show) {
    const overlay = document.getElementById("loading-overlay");
    if (show) {
        overlay.classList.add("active");
    } else {
        overlay.classList.remove("active");
    }
}

function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    const icon = type === "success" ? "✓" : "✗";
    toast.innerHTML = `<span>${icon}</span><p>${message}</p>`;
    container.appendChild(toast);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = "slideIn 0.25s reverse forwards";
        setTimeout(() => toast.remove(), 250);
    }, 4000);
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
    if (num >= 1000) return (num / 1000).toFixed(0) + "k";
    return num;
}

function formatDuration(seconds) {
    if (!seconds) return "—";
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hrs > 0) {
        return `${hrs}h ${mins}m`;
    }
    return `${mins}:${secs.toString().padStart(2, "0")}`;
}
