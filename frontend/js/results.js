// Configuration
const API_URL = 'http://localhost:8000/api';

// DOM Elements
const scorePercentage = document.getElementById('scorePercentage');
const scoreCircle = document.getElementById('scoreCircle');
const correctCount = document.getElementById('correctCount');
const incorrectCount = document.getElementById('incorrectCount');
const unattemptedCount = document.getElementById('unattemptedCount');
const totalQuestions = document.getElementById('totalQuestions');
const completionDate = document.getElementById('completionDate');
const weakTopicsContainer = document.getElementById('weakTopicsContainer');
const studyPlanContainer = document.getElementById('studyPlanContainer');

// Load results
async function loadResults() {
    // Get submission ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const submissionId = urlParams.get('id');
    
    if (!submissionId) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    try {
        // Fetch results data
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = 'index.html';
            return;
        }
        
        const response = await fetch(`${API_URL}/analysis/${submissionId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('access_token');
                window.location.href = 'index.html';
                return;
            }
            throw new Error('Failed to fetch results');
        }
        
        const results = await response.json();
        displayResults(results);
        
    } catch (error) {
        console.error('Error loading results:', error);
        alert('Failed to load results. Please try again later.');
        window.location.href = 'dashboard.html';
    }
}

// Display results
function displayResults(results) {
    // Calculate score percentage
    const score = results.score;
    
    // Update score circle
    scorePercentage.textContent = `${Math.round(score)}%`;
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (score / 100) * circumference;
    scoreCircle.style.strokeDasharray = circumference;
    scoreCircle.style.strokeDashoffset = offset;
    
    // Update counts
    correctCount.textContent = results.correct_answers;
    incorrectCount.textContent = results.incorrect_answers;
    unattemptedCount.textContent = results.unattempted;
    totalQuestions.textContent = results.total_questions;
    
    // Format date
    const now = new Date();
    completionDate.textContent = now.toLocaleDateString();
    
    // Display weak topics
    displayWeakTopics(results.weak_topics);
    
    // Display study plan
    displayStudyPlan(results.study_plan);
}

// Display weak topics
function displayWeakTopics(weakTopics) {
    if (!weakTopicsContainer) return;
    
    weakTopicsContainer.innerHTML = '';
    
    if (weakTopics.length === 0) {
        weakTopicsContainer.innerHTML = '<p class="text-gray-700">Great job! No major areas of weakness detected.</p>';
        return;
    }
    
    // Create a list of weak topics
    const topicList = document.createElement('ul');
    topicList.className = 'space-y-2';
    
    weakTopics.forEach(topic => {
        const listItem = document.createElement('li');
        listItem.className = 'flex items-center';
        
        // Create badge with subject
        const badge = document.createElement('span');
        badge.className = 'bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-1 rounded mr-2';
        badge.textContent = topic.subject;
        
        // Create topic text
        const topicText = document.createElement('span');
        topicText.className = 'text-gray-700';
        topicText.textContent = topic.topic;
        
        listItem.appendChild(badge);
        listItem.appendChild(topicText);
        topicList.appendChild(listItem);
    });
    
    weakTopicsContainer.appendChild(topicList);
}

// Display study plan
function displayStudyPlan(studyPlan) {
    if (!studyPlanContainer) return;
    
    if (!studyPlan) {
        studyPlanContainer.innerHTML = '<p class="text-gray-700">Study plan is not available.</p>';
        return;
    }
    
    // Use marked.js to render markdown
    studyPlanContainer.innerHTML = marked.parse(studyPlan);
}

// Event listeners
document.addEventListener('DOMContentLoaded', loadResults);
