/* =============================================
   CLIMATEWISE DASHBOARD CHARTS JS
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {
    if (typeof dashboardData === 'undefined') return;

    initDonationsChart();
    initMembersChart();
});

function initDonationsChart() {
    const ctx = document.getElementById('donationsChart');
    if (!ctx) return;

    const labels = dashboardData.donations.labels;
    const data = dashboardData.donations.data;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Donations (GH₵)',
                data,
                borderColor: '#027729',
                backgroundColor: 'rgba(2, 119, 41, 0.08)',
                borderWidth: 2.5,
                pointBackgroundColor: '#027729',
                pointRadius: 4,
                pointHoverRadius: 7,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { intersect: false, mode: 'index' },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1a2e1c',
                    titleColor: '#fff',
                    bodyColor: 'rgba(255,255,255,0.7)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => ' GH₵' + ctx.parsed.y.toLocaleString()
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(0,0,0,0.04)' },
                    ticks: {
                        color: '#6b8070',
                        font: { family: 'DM Sans', size: 11 }
                    }
                },
                y: {
                    grid: { color: 'rgba(0,0,0,0.04)' },
                    ticks: {
                        color: '#6b8070',
                        font: { family: 'DM Sans', size: 11 },
                        callback: val => 'GH₵' + val.toLocaleString()
                    }
                }
            }
        }
    });
}

function initMembersChart() {
    const ctx = document.getElementById('membersChart');
    if (!ctx) return;

    const volunteers = dashboardData.members.volunteers;
    const partners = dashboardData.members.partners;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Volunteers', 'Partners'],
            datasets: [{
                data: [volunteers, partners],
                backgroundColor: ['#027729', '#0096c7'],
                hoverBackgroundColor: ['#2d5016', '#005f87'],
                borderWidth: 0,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1a2e1c',
                    titleColor: '#fff',
                    bodyColor: 'rgba(255,255,255,0.7)',
                    padding: 12,
                    cornerRadius: 8
                }
            }
        }
    });
}