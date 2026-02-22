/* =============================================
   CLIMATEWISE ADMIN JS
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
    initTopbar();
    animateCounters();
    animateProgressBars();
    initChartTabs();
    initActivityRefresh();
    autoHideAlerts();
});

// ---- SIDEBAR TOGGLE ----
function initSidebar() {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('adminSidebar');
    const main = document.getElementById('adminMain');

    if (!toggle || !sidebar) return;

    toggle.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            sidebar.classList.toggle('open');
        } else {
            const isCollapsed = sidebar.style.width === '0px';
            if (isCollapsed) {
                sidebar.style.width = '260px';
                sidebar.style.overflow = 'visible';
                if (main) main.style.marginLeft = '260px';
            } else {
                sidebar.style.width = '0px';
                sidebar.style.overflow = 'hidden';
                if (main) main.style.marginLeft = '0px';
            }
        }
    });

    // Close on overlay click (mobile)
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 &&
            sidebar.classList.contains('open') &&
            !sidebar.contains(e.target) &&
            !toggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    });
}

// ---- TOPBAR DATE ----
function initTopbar() {
    const dateEl = document.getElementById('currentDate');
    if (!dateEl) return;

    const now = new Date();
    const opts = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
    dateEl.textContent = now.toLocaleDateString('en-US', opts);
}

// ---- COUNT ANIMATION ----
function animateCounters() {
    const counters = document.querySelectorAll('[data-count]');
    counters.forEach(el => {
        const target = parseFloat(el.dataset.count) || 0;
        const isCurrency = el.classList.contains('currency');
        const duration = 1400;
        const steps = 60;
        const increment = target / steps;
        let current = 0;
        let step = 0;

        const ease = t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

        const timer = setInterval(() => {
            step++;
            current = target * ease(step / steps);
            if (isCurrency) {
                el.textContent = 'GH₵' + formatNumber(Math.round(current));
            } else {
                el.textContent = Math.round(current).toLocaleString();
            }
            if (step >= steps) {
                clearInterval(timer);
                if (isCurrency) {
                    el.textContent = 'GH₵' + formatNumber(target);
                } else {
                    el.textContent = Math.round(target).toLocaleString();
                }
            }
        }, duration / steps);
    });
}

function formatNumber(n) {
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
    return n.toLocaleString();
}

// ---- PROGRESS BARS ----
function animateProgressBars() {
    const bars = document.querySelectorAll('.progress-bar-fill');
    setTimeout(() => {
        bars.forEach(bar => {
            const target = bar.style.width;
            bar.style.setProperty('--target-width', target);
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = target;
            }, 100);
        });
    }, 300);
}

// ---- CHART TABS ----
function initChartTabs() {
    const tabs = document.querySelectorAll('.chart-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const target = tab.dataset.target;
            document.querySelectorAll('.chart-wrapper').forEach(w => {
                w.classList.add('hidden');
            });

            const targetWrap = document.getElementById(target + 'Wrap');
            if (targetWrap) targetWrap.classList.remove('hidden');
        });
    });
}

// ---- ACTIVITY REFRESH ----
function initActivityRefresh() {
    const btn = document.getElementById('refreshActivity');
    if (!btn) return;

    btn.addEventListener('click', async () => {
        btn.classList.add('spinning');

        try {
            const res = await fetch('/admin/api/activity');
            if (!res.ok) throw new Error();
            const data = await res.json();
            renderActivity(data.activities);
        } catch {
            // silently fail - keep existing content
        } finally {
            setTimeout(() => btn.classList.remove('spinning'), 600);
        }
    });
}

function renderActivity(activities) {
    const feed = document.getElementById('activityFeed');
    if (!feed) return;

    if (!activities || activities.length === 0) {
        feed.innerHTML = `
            <div class="activity-empty">
                <i class="fas fa-leaf"></i>
                <p>No recent activity yet.<br>Your community is growing!</p>
            </div>`;
        return;
    }

    const iconMap = {
        volunteer: 'fa-user-plus',
        partner: 'fa-handshake',
        donation: 'fa-heart',
        message: 'fa-envelope'
    };

    feed.innerHTML = activities.map(a => `
        <div class="activity-item" style="animation: fadeInUp 0.3s ease">
            <div class="activity-icon icon-${a.type}">
                <i class="fas ${iconMap[a.type] || 'fa-circle'}"></i>
            </div>
            <div class="activity-body">
                <p class="activity-text">${escapeHtml(a.text)}</p>
                <span class="activity-time">
                    <i class="fas fa-clock"></i> ${escapeHtml(a.time_ago)}
                </span>
            </div>
            <div class="activity-badge badge-${a.type}">${a.type}</div>
        </div>
    `).join('');
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ---- AUTO HIDE ALERTS ----
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.admin-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            alert.style.transition = 'all 0.4s ease';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });
}