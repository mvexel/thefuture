/**
 * The Future Predictor - Web Frontend JavaScript
 * Iteration 10
 */

// API Base URL
const API_BASE = '';

// State
let currentPrediction = null;

// DOM Elements
const elements = {
    tabs: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),
    themeSelect: document.getElementById('theme-select'),
    categorySelect: document.getElementById('category-select'),
    timeAware: document.getElementById('time-aware'),
    smartMode: document.getElementById('smart-mode'),
    saveHistory: document.getElementById('save-history'),
    predictBtn: document.getElementById('predict-btn'),
    predictionResult: document.getElementById('prediction-result'),
    historyList: document.getElementById('history-list'),
    historyCategoryFilter: document.getElementById('history-category-filter'),
    ratedOnly: document.getElementById('rated-only'),
    refreshHistory: document.getElementById('refresh-history'),
    statsContent: document.getElementById('stats-content'),
    themesGrid: document.getElementById('themes-grid'),
    refreshThemes: document.getElementById('refresh-themes'),
    remindersList: document.getElementById('reminders-list'),
    showAllReminders: document.getElementById('show-all-reminders'),
    refreshReminders: document.getElementById('refresh-reminders'),
    reminderModal: document.getElementById('reminder-modal'),
    reminderDate: document.getElementById('reminder-date'),
    saveReminderBtn: document.getElementById('save-reminder-btn'),
    cancelReminderBtn: document.getElementById('cancel-reminder-btn'),
    shareModal: document.getElementById('share-modal'),
    shareText: document.getElementById('share-text'),
    copyShareBtn: document.getElementById('copy-share-btn'),
    closeShareBtn: document.getElementById('close-share-btn'),
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadCategories();
    loadThemes();
    loadHistory();
    loadStats();
    loadReminders();
    initEventListeners();
    setDefaultReminderDate();
});

// Tab Navigation
function initTabs() {
    elements.tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.dataset.tab;
            
            // Update active tab button
            elements.tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update active tab content
            elements.tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });

            // Refresh data when switching tabs
            if (tabId === 'history') loadHistory();
            if (tabId === 'stats') loadStats();
            if (tabId === 'themes') loadThemes();
            if (tabId === 'reminders') loadReminders();
        });
    });
}

// Event Listeners
function initEventListeners() {
    // Predict button
    elements.predictBtn.addEventListener('click', getPrediction);

    // History controls
    elements.refreshHistory.addEventListener('click', loadHistory);
    elements.historyCategoryFilter.addEventListener('change', loadHistory);
    elements.ratedOnly.addEventListener('change', loadHistory);

    // Themes
    elements.refreshThemes.addEventListener('click', loadThemes);

    // Reminders
    elements.refreshReminders.addEventListener('click', loadReminders);
    elements.showAllReminders.addEventListener('change', loadReminders);

    // Modal buttons
    elements.saveReminderBtn.addEventListener('click', saveReminder);
    elements.cancelReminderBtn.addEventListener('click', () => elements.reminderModal.classList.add('hidden'));
    elements.copyShareBtn.addEventListener('click', copyShareText);
    elements.closeShareBtn.addEventListener('click', () => elements.shareModal.classList.add('hidden'));

    // Share buttons (delegated)
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('share-btn')) {
            const format = e.target.dataset.format;
            showShareModal(format);
        }
        if (e.target.classList.contains('remind-btn')) {
            elements.reminderModal.classList.remove('hidden');
        }
        if (e.target.classList.contains('use-theme-btn')) {
            const theme = e.target.dataset.theme;
            useTheme(theme);
        }
        if (e.target.classList.contains('acknowledge-btn')) {
            const reminderId = parseInt(e.target.dataset.id);
            acknowledgeReminder(reminderId);
        }
        if (e.target.classList.contains('rate-btn')) {
            const predId = parseInt(e.target.dataset.id);
            ratePrediction(predId);
        }
    });

    // Close modal on backdrop click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    });
}

// Load Categories
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`);
        const categories = await response.json();
        
        elements.categorySelect.innerHTML = '<option value="">Random</option>';
        elements.historyCategoryFilter.innerHTML = '<option value="">All Categories</option>';
        
        categories.forEach(cat => {
            elements.categorySelect.innerHTML += `<option value="${cat}">${capitalize(cat)}</option>`;
            elements.historyCategoryFilter.innerHTML += `<option value="${cat}">${capitalize(cat)}</option>`;
        });
    } catch (error) {
        console.error('Failed to load categories:', error);
    }
}

// Load Themes
async function loadThemes() {
    try {
        const response = await fetch(`${API_BASE}/themes`);
        const themes = await response.json();
        
        // Update theme select
        elements.themeSelect.innerHTML = '<option value="">Default</option>';
        Object.keys(themes).forEach(theme => {
            elements.themeSelect.innerHTML += `<option value="${theme}">${capitalize(theme)}</option>`;
        });

        // Update themes grid
        elements.themesGrid.innerHTML = '';
        Object.entries(themes).forEach(([name, categories]) => {
            const card = document.createElement('div');
            card.className = 'theme-card';
            card.innerHTML = `
                <h4>${name}</h4>
                <div class="categories">
                    ${categories.map(cat => `<span class="category-tag">${cat}</span>`).join('')}
                </div>
                <button class="use-theme-btn" data-theme="${name}">Use This Theme</button>
            `;
            elements.themesGrid.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to load themes:', error);
        elements.themesGrid.innerHTML = '<p class="empty-state">Failed to load themes</p>';
    }
}

// Get Prediction
async function getPrediction() {
    const theme = elements.themeSelect.value;
    const category = elements.categorySelect.value;
    const timeAware = elements.timeAware.checked;
    const smart = elements.smartMode.checked;
    const save = elements.saveHistory.checked;

    const params = new URLSearchParams();
    if (theme) params.append('theme', theme);
    if (category) params.append('category', category);
    if (timeAware) params.append('time_aware', 'true');
    if (smart) params.append('smart', 'true');
    params.append('save', save.toString());

    elements.predictBtn.disabled = true;
    elements.predictBtn.textContent = '🔮 Loading...';

    try {
        const response = await fetch(`${API_BASE}/predict?${params}`);
        currentPrediction = await response.json();
        displayPrediction(currentPrediction);
    } catch (error) {
        console.error('Failed to get prediction:', error);
        alert('Failed to get prediction. Please try again.');
    } finally {
        elements.predictBtn.disabled = false;
        elements.predictBtn.textContent = '🔮 Get Prediction';
    }
}

// Display Prediction
function displayPrediction(prediction) {
    const result = elements.predictionResult;
    result.classList.remove('hidden');

    result.querySelector('.prediction-text').textContent = `🌟 ${prediction.prediction}`;
    result.querySelector('.category-badge').textContent = capitalize(prediction.category);
    result.querySelector('.confidence').textContent = `Confidence: ${prediction.confidence}`;
    result.querySelector('.prediction-date').textContent = `📅 Applies to: ${prediction.applies_to}`;

    const themeBadge = result.querySelector('.theme-badge');
    if (prediction.theme) {
        themeBadge.textContent = capitalize(prediction.theme);
        themeBadge.classList.remove('hidden');
    } else {
        themeBadge.classList.add('hidden');
    }
}

// Load History
async function loadHistory() {
    const category = elements.historyCategoryFilter.value;
    const ratedOnly = elements.ratedOnly.checked;

    const params = new URLSearchParams();
    params.append('count', '50');
    if (category) params.append('category', category);
    if (ratedOnly) params.append('rated_only', 'true');

    try {
        const response = await fetch(`${API_BASE}/history?${params}`);
        const history = await response.json();

        if (history.length === 0) {
            elements.historyList.innerHTML = '<p class="empty-state">No predictions found</p>';
            return;
        }

        elements.historyList.innerHTML = history.reverse().map(pred => `
            <div class="history-item">
                <div class="prediction-text">${pred.prediction}</div>
                <div class="meta">
                    <span>ID: ${pred.id || 'N/A'}</span>
                    <span>Category: ${capitalize(pred.category || 'unknown')}</span>
                    ${pred.rating ? `<span class="rating">★ ${pred.rating}/5</span>` : `<button class="rate-btn" data-id="${pred.id}">Rate</button>`}
                    ${pred.generated_at ? `<span>${formatDate(pred.generated_at)}</span>` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load history:', error);
        elements.historyList.innerHTML = '<p class="empty-state">Failed to load history</p>';
    }
}

// Load Stats
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const stats = await response.json();

        if (stats.total_predictions === 0) {
            elements.statsContent.innerHTML = '<p class="empty-state">No predictions yet. Start predicting!</p>';
            return;
        }

        let html = `
            <div class="stat-card">
                <h3>Total Predictions</h3>
                <div class="stat-value">${stats.total_predictions}</div>
            </div>
        `;

        if (stats.ratings && stats.ratings.count) {
            html += `
                <div class="stat-card">
                    <h3>Rated Predictions</h3>
                    <div class="stat-value">${stats.ratings.count}</div>
                    <div class="stat-detail">Avg: ★ ${stats.ratings.average}/5</div>
                </div>
            `;
        }

        if (stats.categories && Object.keys(stats.categories).length > 0) {
            const maxCount = Math.max(...Object.values(stats.categories));
            html += `
                <div class="stat-card category-breakdown">
                    <h3>Predictions by Category</h3>
                    ${Object.entries(stats.categories)
                        .sort((a, b) => b[1] - a[1])
                        .map(([cat, count]) => `
                            <div class="category-bar">
                                <span class="label">${capitalize(cat)}</span>
                                <div class="bar">
                                    <div class="bar-fill" style="width: ${(count / maxCount) * 100}%"></div>
                                </div>
                                <span class="count">${count}</span>
                            </div>
                        `).join('')}
                </div>
            `;
        }

        elements.statsContent.innerHTML = html;
    } catch (error) {
        console.error('Failed to load stats:', error);
        elements.statsContent.innerHTML = '<p class="empty-state">Failed to load stats</p>';
    }
}

// Load Reminders
async function loadReminders() {
    const showAll = elements.showAllReminders.checked;

    try {
        const response = await fetch(`${API_BASE}/reminders?show_all=${showAll}`);
        const reminders = await response.json();

        if (reminders.length === 0) {
            elements.remindersList.innerHTML = '<p class="empty-state">No reminders found</p>';
            return;
        }

        const today = new Date().toISOString().split('T')[0];

        elements.remindersList.innerHTML = reminders.map(reminder => {
            let statusClass = '';
            let statusText = '';
            
            if (reminder.acknowledged) {
                statusClass = 'acknowledged';
                statusText = '✅ Done';
            } else if (reminder.remind_date < today) {
                statusClass = 'overdue';
                statusText = '⚠️ Overdue';
            } else if (reminder.remind_date === today) {
                statusClass = 'today';
                statusText = '📅 Today';
            } else {
                statusText = `🗓️ ${reminder.remind_date}`;
            }

            return `
                <div class="reminder-item ${statusClass}">
                    <span class="status">${statusText}</span>
                    <div class="prediction-text">🔮 ${reminder.prediction}</div>
                    <div class="meta">
                        Category: ${capitalize(reminder.category || 'unknown')} | 
                        Reminder ID: ${reminder.reminder_id}
                    </div>
                    ${!reminder.acknowledged ? `<button class="acknowledge-btn" data-id="${reminder.reminder_id}">✓ Acknowledge</button>` : ''}
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Failed to load reminders:', error);
        elements.remindersList.innerHTML = '<p class="empty-state">Failed to load reminders</p>';
    }
}

// Save Reminder
async function saveReminder() {
    if (!currentPrediction) {
        alert('No prediction to set reminder for');
        return;
    }

    const date = elements.reminderDate.value;
    if (!date) {
        alert('Please select a date');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/reminders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prediction_id: currentPrediction.id,
                prediction: currentPrediction.prediction,
                category: currentPrediction.category,
                remind_date: date
            })
        });

        if (response.ok) {
            alert('Reminder saved!');
            elements.reminderModal.classList.add('hidden');
            loadReminders();
        } else {
            const error = await response.json();
            alert(`Failed to save reminder: ${error.detail}`);
        }
    } catch (error) {
        console.error('Failed to save reminder:', error);
        alert('Failed to save reminder');
    }
}

// Acknowledge Reminder
async function acknowledgeReminder(reminderId) {
    try {
        const response = await fetch(`${API_BASE}/reminders/${reminderId}/acknowledge`, {
            method: 'POST'
        });

        if (response.ok) {
            loadReminders();
        } else {
            const error = await response.json();
            alert(`Failed to acknowledge: ${error.detail}`);
        }
    } catch (error) {
        console.error('Failed to acknowledge reminder:', error);
        alert('Failed to acknowledge reminder');
    }
}

// Rate Prediction
async function ratePrediction(predictionId) {
    const rating = prompt('Rate this prediction (1-5 stars):');
    if (!rating) return;

    const ratingNum = parseInt(rating);
    if (isNaN(ratingNum) || ratingNum < 1 || ratingNum > 5) {
        alert('Please enter a number between 1 and 5');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prediction_id: predictionId,
                rating: ratingNum
            })
        });

        if (response.ok) {
            loadHistory();
            loadStats();
        } else {
            const error = await response.json();
            alert(`Failed to rate: ${error.detail}`);
        }
    } catch (error) {
        console.error('Failed to rate prediction:', error);
        alert('Failed to rate prediction');
    }
}

// Use Theme
function useTheme(theme) {
    elements.themeSelect.value = theme;
    // Switch to predict tab
    document.querySelector('[data-tab="predict"]').click();
}

// Show Share Modal
function showShareModal(format) {
    if (!currentPrediction) return;

    let text = '';
    const pred = currentPrediction;

    if (format === 'twitter') {
        const hashtag = `#${capitalize(pred.category).replace(/\s/g, '')}`;
        text = `🔮 ${pred.prediction}\n\n${hashtag} #TheFuturePredictor`;
    } else if (format === 'markdown') {
        text = `## 🔮 My Fortune\n\n> ${pred.prediction}\n\n**Category**: ${capitalize(pred.category)} | **Applies to**: ${pred.applies_to} | **Confidence**: ${pred.confidence}\n\n*Generated by The Future Predictor*`;
    } else {
        text = `🔮 ${pred.prediction}\n\n📅 Applies to: ${pred.applies_to}\n🎯 Category: ${capitalize(pred.category)}\n💫 Confidence: ${pred.confidence}\n\n— The Future Predictor`;
    }

    elements.shareText.value = text;
    elements.shareModal.classList.remove('hidden');
}

// Copy Share Text
async function copyShareText() {
    const text = elements.shareText.value;
    
    try {
        await navigator.clipboard.writeText(text);
        elements.copyShareBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            elements.copyShareBtn.textContent = '📋 Copy';
        }, 2000);
    } catch (error) {
        // Fallback for older browsers
        elements.shareText.select();
        document.execCommand('copy');
        elements.copyShareBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            elements.copyShareBtn.textContent = '📋 Copy';
        }, 2000);
    }
}

// Set Default Reminder Date (tomorrow)
function setDefaultReminderDate() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    elements.reminderDate.value = tomorrow.toISOString().split('T')[0];
    elements.reminderDate.min = new Date().toISOString().split('T')[0];
}

// Utility Functions
function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(isoString) {
    try {
        const date = new Date(isoString);
        return date.toLocaleString();
    } catch {
        return isoString;
    }
}
