// Configuration
const API_URL = 'http://localhost:8000/api';

// DOM Elements
const usernameElement = document.getElementById('username');
const logoutBtn = document.getElementById('logoutBtn');
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.querySelector('aside');
const testList = document.getElementById('testList');

// State variables
let tests = [];

// Set username from localStorage
document.addEventListener('DOMContentLoaded', function() {
    const username = localStorage.getItem('username');
    if (usernameElement) {
        usernameElement.textContent = username || 'User';
    }
    
    // Load available tests
    loadTests();
    
    // Event listeners
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
        });
    }
    
    // Add event listeners for tabs
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.id || this.id !== 'logoutBtn') {
                e.preventDefault();
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
});

// Load tests from the API
async function loadTests() {
    try {
        const token = localStorage.getItem('token');
        
        if (!token) {
            console.error('No authentication token found');
            return;
        }
        
        const response = await fetch(`${API_URL}/tests`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            tests = data;
            renderTests();
        } else {
            console.error('Failed to load tests:', await response.text());
        }
    } catch (error) {
        console.error('Error loading tests:', error);
    }
}

// Render tests in the UI
function renderTests() {
    if (!testList) return;
    
    if (tests.length === 0) {
        testList.innerHTML = `
            <div class="text-center p-8 text-gray-500">
                <p>No tests available at the moment.</p>
            </div>
        `;
        return;
    }
    
    testList.innerHTML = tests.map(test => `
        <div class="bg-white rounded-lg shadow-md overflow-hidden dashboard-card">
            <div class="bg-blue-50 p-4 border-b border-blue-100">
                <h3 class="text-lg font-semibold text-blue-800">${test.title}</h3>
                <div class="flex items-center space-x-2 mt-1">
                    <span class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">${test.subjects.join(', ')}</span>
                    <span class="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full">${test.difficulty}</span>
                    <span class="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">${test.duration} min</span>
                </div>
            </div>
            <div class="p-4">
                <p class="text-gray-600 text-sm mb-4">${test.description}</p>
                <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-500">${test.total_questions} questions</span>
                    <a href="/test?id=${test.id}" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
                        Start Test
                    </a>
                </div>
            </div>
        </div>
    `).join('');
}

// Logout function from auth.js
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/';
}
