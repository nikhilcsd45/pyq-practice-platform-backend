// Configuration
const API_URL = 'http://localhost:8000/api';

// State variables
let test = null;
let currentQuestionIndex = 0;
let userAnswers = [];
let timerInterval = null;
let startTime = null;
let testDuration = 0; // in minutes

// DOM Elements
const testTitle = document.getElementById('testTitle');
const questionNumber = document.getElementById('questionNumber');
const questionText = document.getElementById('questionText');
const optionsContainer = document.getElementById('optionsContainer');
const questionDifficulty = document.getElementById('questionDifficulty');
const prevButton = document.getElementById('prevButton');
const nextButton = document.getElementById('nextButton');
const questionNav = document.getElementById('questionNav');
const timerElement = document.getElementById('timer');
const submitTestButton = document.getElementById('submitTest');
const submitModal = document.getElementById('submitModal');
const cancelSubmitButton = document.getElementById('cancelSubmit');
const confirmSubmitButton = document.getElementById('confirmSubmit');
const unansweredCountElement = document.getElementById('unansweredCount');

// Initialize test
async function initTest() {
    // Get test ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const testId = urlParams.get('id');
    
    if (!testId) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    try {
        // Fetch test data
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = 'index.html';
            return;
        }
        
        const response = await fetch(`${API_URL}/tests/${testId}`, {
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
            throw new Error('Failed to fetch test');
        }
        
        test = await response.json();
        
        // Initialize test UI
        initializeTestUI();
        
        // Initialize user answers array
        initializeUserAnswers();
        
        // Load first question
        loadQuestion(0);
        
        // Start timer
        startTimer();
        
    } catch (error) {
        console.error('Error initializing test:', error);
        alert('Failed to load test. Please try again later.');
        window.location.href = 'dashboard.html';
    }
}

// Initialize test UI
function initializeTestUI() {
    testTitle.textContent = test.title;
    testDuration = test.duration;
    
    // Create question navigation
    questionNav.innerHTML = '';
    for (let i = 0; i < test.questions.length; i++) {
        const questionBubble = document.createElement('div');
        questionBubble.classList.add('h-8', 'w-8', 'rounded-full', 'flex', 'items-center', 'justify-center', 'bg-gray-300', 'cursor-pointer', 'question-bubble');
        questionBubble.textContent = i + 1;
        questionBubble.setAttribute('data-index', i);
        
        questionBubble.addEventListener('click', () => loadQuestion(i));
        
        questionNav.appendChild(questionBubble);
    }
    
    // Update navigation for first question
    updateQuestionNavigation(0);
}

// Initialize user answers
function initializeUserAnswers() {
    userAnswers = test.questions.map(() => null);
}

// Load question by index
function loadQuestion(index) {
    if (!test || index < 0 || index >= test.questions.length) return;
    
    currentQuestionIndex = index;
    const question = test.questions[index];
    
    // Update question UI
    questionNumber.textContent = `Question ${index + 1} of ${test.questions.length}`;
    questionText.textContent = question.text;
    questionDifficulty.textContent = question.difficulty;
    
    // Load options
    optionsContainer.innerHTML = '';
    question.options.forEach(option => {
        const optionElement = document.createElement('div');
        optionElement.classList.add('p-4', 'border', 'rounded-lg', 'option-container', 'cursor-pointer');
        optionElement.setAttribute('data-option-id', option.id);
        
        // Check if this option is selected by user
        if (userAnswers[index] === option.id) {
            optionElement.classList.add('selected');
        }
        
        optionElement.innerHTML = `
            <div class="flex items-start">
                <div class="flex-shrink-0 mr-2 mt-0.5">
                    <div class="w-5 h-5 border border-gray-400 rounded-full flex items-center justify-center ${userAnswers[index] === option.id ? 'bg-blue-600 border-blue-600' : ''}">
                        ${userAnswers[index] === option.id ? '<span class="text-white text-xs">✓</span>' : ''}
                    </div>
                </div>
                <div>
                    <span class="font-medium">${option.id.toUpperCase()}.</span> ${option.text}
                </div>
            </div>
        `;
        
        optionElement.addEventListener('click', () => selectOption(option.id));
        
        optionsContainer.appendChild(optionElement);
    });
    
    // Update navigation buttons
    prevButton.disabled = index === 0;
    nextButton.textContent = index === test.questions.length - 1 ? 'Finish' : 'Next';
    
    // Update question navigation
    updateQuestionNavigation(index);
}

// Select an answer option
function selectOption(optionId) {
    // Update user answer
    userAnswers[currentQuestionIndex] = optionId;
    
    // Update UI
    const options = document.querySelectorAll('.option-container');
    options.forEach(option => {
        if (option.getAttribute('data-option-id') === optionId) {
            option.classList.add('selected');
            
            // Update checkbox
            const checkbox = option.querySelector('div.w-5');
            checkbox.classList.add('bg-blue-600', 'border-blue-600');
            checkbox.innerHTML = '<span class="text-white text-xs">✓</span>';
        } else {
            option.classList.remove('selected');
            
            // Update checkbox
            const checkbox = option.querySelector('div.w-5');
            checkbox.classList.remove('bg-blue-600', 'border-blue-600');
            checkbox.innerHTML = '';
        }
    });
    
    // Update question navigation
    updateQuestionNavigation(currentQuestionIndex);
}

// Update question navigation UI
function updateQuestionNavigation(currentIndex) {
    const questionBubbles = document.querySelectorAll('.question-bubble');
    
    questionBubbles.forEach((bubble, index) => {
        // Remove all status classes
        bubble.classList.remove('bg-blue-600', 'bg-green-600', 'bg-gray-300', 'text-white');
        
        if (index === currentIndex) {
            // Current question
            bubble.classList.add('bg-blue-600', 'text-white');
        } else if (userAnswers[index] !== null) {
            // Answered question
            bubble.classList.add('bg-green-600', 'text-white');
        } else {
            // Unanswered question
            bubble.classList.add('bg-gray-300');
        }
    });
}

// Format time for display
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    return [
        hours.toString().padStart(2, '0'),
        minutes.toString().padStart(2, '0'),
        secs.toString().padStart(2, '0')
    ].join(':');
}

// Start test timer
function startTimer() {
    startTime = Date.now();
    const endTime = startTime + (testDuration * 60 * 1000);
    
    function updateTimer() {
        const now = Date.now();
        const timeLeft = Math.max(0, Math.floor((endTime - now) / 1000));
        
        timerElement.textContent = formatTime(timeLeft);
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            submitTest(true); // Auto-submit when time runs out
        }
    }
    
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);
}

// Show submission confirmation
function showSubmissionConfirmation() {
    // Count unanswered questions
    const unansweredCount = userAnswers.filter(ans => ans === null).length;
    unansweredCountElement.textContent = unansweredCount;
    
    // Show modal
    submitModal.classList.remove('hidden');
}

// Submit test
async function submitTest(isAutoSubmit = false) {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    if (!isAutoSubmit) {
        submitModal.classList.add('hidden');
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username');
        
        if (!token || !username) {
            window.location.href = 'index.html';
            return;
        }
        
        // Prepare submission data
        const answers = [];
        test.questions.forEach((question, index) => {
            if (userAnswers[index] !== null) {
                answers.push({
                    question_id: question.id,
                    selected_option_id: userAnswers[index]
                });
            }
        });
        
        const submissionData = {
            test_id: test.id,
            username: username,
            answers: answers
        };
        
        // Submit to API
        const response = await fetch(`${API_URL}/tests/${test.id}/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(submissionData)
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                window.location.href = 'index.html';
                return;
            }
            throw new Error('Failed to submit test');
        }
        
        const result = await response.json();
        
        // Redirect to results page
        window.location.href = `results.html?id=${result.submission_id}`;
        
    } catch (error) {
        console.error('Error submitting test:', error);
        alert('Failed to submit test. Please try again.');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    initTest();
    
    // Previous button
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            if (currentQuestionIndex > 0) {
                loadQuestion(currentQuestionIndex - 1);
            }
        });
    }
    
    // Next button
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (currentQuestionIndex < test.questions.length - 1) {
                loadQuestion(currentQuestionIndex + 1);
            } else {
                // On last question
                showSubmissionConfirmation();
            }
        });
    }
    
    // Submit test button
    if (submitTestButton) {
        submitTestButton.addEventListener('click', showSubmissionConfirmation);
    }
    
    // Cancel submission
    if (cancelSubmitButton) {
        cancelSubmitButton.addEventListener('click', () => {
            submitModal.classList.add('hidden');
        });
    }
    
    // Confirm submission
    if (confirmSubmitButton) {
        confirmSubmitButton.addEventListener('click', () => submitTest());
    }
});
