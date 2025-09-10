// Handle login form submission
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const loginError = document.getElementById('loginError');
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        'username': username,
                        'password': password
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Store token in localStorage
                    localStorage.setItem('token', data.access_token);
                    localStorage.setItem('username', username);
                    
                    // Redirect to dashboard
                    window.location.href = '/dashboard';
                } else {
                    // Show error message
                    loginError.classList.remove('hidden');
                }
            } catch (error) {
                console.error('Login error:', error);
                loginError.classList.remove('hidden');
            }
        });
    }
});

// Check if user is already logged in
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    
    // If we're on login or signup page and already have a token, redirect to dashboard
    if (token && (window.location.pathname === '/' || window.location.pathname === '/index.html' || window.location.pathname === '/signup')) {
        window.location.href = '/dashboard';
    }
    
    // If we're on any other page and don't have a token, redirect to login
    if (!token && 
        window.location.pathname !== '/' && 
        window.location.pathname !== '/index.html' && 
        window.location.pathname !== '/signup' && 
        window.location.pathname !== '/signup.html') {
        window.location.href = '/';
    }
}

// Handle signup form submission
document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const signupError = document.getElementById('signupError');
            
            // Check if passwords match
            if (password !== confirmPassword) {
                signupError.textContent = 'Passwords do not match.';
                signupError.classList.remove('hidden');
                return;
            }
            
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username,
                        email,
                        password
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Show success and redirect to login after a brief delay
                    document.getElementById('signupSuccess').classList.remove('hidden');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    // Show error message
                    signupError.textContent = data.detail || 'Registration failed. Please try again.';
                    signupError.classList.remove('hidden');
                }
            } catch (error) {
                console.error('Signup error:', error);
                signupError.textContent = 'An error occurred. Please try again.';
                signupError.classList.remove('hidden');
            }
        });
    }
});

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

// Check auth status on page load
document.addEventListener('DOMContentLoaded', checkAuthStatus);
