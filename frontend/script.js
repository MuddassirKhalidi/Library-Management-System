// API Base URL - can be configured in the UI
let API_BASE_URL = 'http://localhost:8000';

// Current user session
let currentUser = null;
let authEmail = null;
let authPassword = null;

// Update API URL when user changes it
document.getElementById('apiUrl').addEventListener('change', (e) => {
    API_BASE_URL = e.target.value.trim() || 'http://localhost:8000';
});

// Authentication Functions
async function login() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value.trim();
    
    if (!email || !password) {
        showError('Please enter both email and password');
        return;
    }
    
    try {
        const data = await apiCall('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
            headers: { 'Content-Type': 'application/json' }
        });
        
        currentUser = data.user;
        authEmail = email;
        authPassword = password;
        
        // Update UI
        document.getElementById('logged-in-user').textContent = `${currentUser.name} (${currentUser.email})`;
        document.getElementById('logged-in-role').textContent = currentUser.role;
        document.querySelector('.login-card').style.display = 'none';
        document.getElementById('user-info').style.display = 'block';
        
        // Show admin buttons
        const adminButtons = document.querySelectorAll('[id$="-btn"]');
        if (currentUser.role === 'librarian' || currentUser.role === 'administrator') {
            adminButtons.forEach(btn => btn.style.display = 'inline-block');
        }
        
        showSuccess('Login successful!');
        hideError();
    } catch (error) {
        showError(error.message || 'Login failed');
        document.getElementById('login-error').textContent = error.message || 'Login failed';
        document.getElementById('login-error').style.display = 'block';
    }
}

function logout() {
    currentUser = null;
    authEmail = null;
    authPassword = null;
    document.querySelector('.login-card').style.display = 'block';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    
    // Hide admin buttons
    document.querySelectorAll('[id$="-btn"]').forEach(btn => btn.style.display = 'none');
    
    // Hide all forms
    document.querySelectorAll('.form-card').forEach(form => form.style.display = 'none');
}

function requireAuth() {
    if (!authEmail || !authPassword) {
        throw new Error('Please login first');
    }
    return { email: authEmail, password: authPassword };
}

// Tab management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// API Helper Functions
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        showLoading();
        hideError();
        hideSuccess();
        
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || `HTTP error! status: ${response.status}`);
        }
        
        hideLoading();
        return data;
    } catch (error) {
        hideLoading();
        throw error;
    }
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = `Error: ${message}`;
    errorDiv.style.display = 'block';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

function showSuccess(message) {
    const successDiv = document.getElementById('success');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    setTimeout(() => {
        hideSuccess();
    }, 5000);
}

function hideSuccess() {
    document.getElementById('success').style.display = 'none';
}

// Books Functions
async function getAllBooks() {
    try {
        const data = await apiCall('/api/books');
        displayBooks(data.books || []);
    } catch (error) {
        showError(error.message);
    }
}

async function searchBooks() {
    const isbn = document.getElementById('search-isbn').value.trim();
    const title = document.getElementById('search-title').value.trim();
    const author = document.getElementById('search-author').value.trim();
    const category = document.getElementById('search-category').value.trim();
    
    if (!isbn && !title && !author && !category) {
        showError('Please enter at least one search criteria');
        return;
    }
    
    try {
        const params = new URLSearchParams();
        if (isbn) params.append('isbn', isbn);
        if (title) params.append('title', title);
        if (author) params.append('author', author);
        if (category) params.append('category', category);
        
        const data = await apiCall(`/api/books/search?${params.toString()}`);
        displayBooks(data.books || []);
        hideSearchBooks();
    } catch (error) {
        showError(error.message);
    }
}

function displayBooks(books) {
    const resultsDiv = document.getElementById('books-results');
    
    if (books.length === 0) {
        resultsDiv.innerHTML = '<div class="empty-state"><p>No books found</p></div>';
        return;
    }
    
    resultsDiv.innerHTML = books.map(book => {
        const isAdmin = currentUser && (currentUser.role === 'librarian' || currentUser.role === 'administrator');
        return `
        <div class="result-card">
            <h3>${book.title || 'Untitled'}</h3>
            <p><strong>ID:</strong> ${book.book_id || 'N/A'}</p>
            <p><strong>ISBN:</strong> ${book.isbn || 'N/A'}</p>
            <p><strong>Authors:</strong> ${book.authors && book.authors.length > 0 ? book.authors.join(', ') : 'N/A'}</p>
            <p><strong>Categories:</strong> ${book.categories && book.categories.length > 0 ? book.categories.join(', ') : 'N/A'}</p>
            <p><strong>Publisher:</strong> ${book.publisher || 'N/A'}</p>
            <p><strong>Year:</strong> ${book.published_year || 'N/A'}</p>
            ${book.description ? `<p><strong>Description:</strong> ${book.description}</p>` : ''}
            ${isAdmin ? `
            <div class="action-buttons">
                <button onclick="showUpdateBookForm(${book.book_id})" class="btn btn-secondary">Update</button>
                <button onclick="deleteBook(${book.book_id})" class="btn btn-warning">Delete</button>
            </div>
            ` : ''}
        </div>
    `}).join('');
}

function showCreateBookForm() {
    document.getElementById('create-book-form').style.display = 'block';
    document.getElementById('update-book-form').style.display = 'none';
}

function hideCreateBookForm() {
    document.getElementById('create-book-form').style.display = 'none';
    document.getElementById('book-isbn').value = '';
    document.getElementById('book-title').value = '';
    document.getElementById('book-publisher').value = '';
    document.getElementById('book-year').value = '';
    document.getElementById('book-description').value = '';
    document.getElementById('book-author-ids').value = '';
    document.getElementById('book-category-ids').value = '';
}

async function createBook() {
    try {
        const auth = requireAuth();
        const authorIds = document.getElementById('book-author-ids').value.trim()
            ? document.getElementById('book-author-ids').value.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id))
            : [];
        const categoryIds = document.getElementById('book-category-ids').value.trim()
            ? document.getElementById('book-category-ids').value.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id))
            : [];
        
        const bookData = {
            isbn: document.getElementById('book-isbn').value.trim(),
            title: document.getElementById('book-title').value.trim(),
            publisher: document.getElementById('book-publisher').value.trim() || null,
            published_year: document.getElementById('book-year').value ? parseInt(document.getElementById('book-year').value) : null,
            description: document.getElementById('book-description').value.trim() || null,
            author_ids: authorIds,
            category_ids: categoryIds
        };
        
        if (!bookData.isbn || !bookData.title) {
            showError('ISBN and Title are required');
            return;
        }
        
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        const data = await apiCall(`/api/books?${params.toString()}`, {
            method: 'POST',
            body: JSON.stringify(bookData),
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Book created successfully!');
        hideCreateBookForm();
        getAllBooks();
    } catch (error) {
        showError(error.message);
    }
}

function showUpdateBookForm(bookId) {
    // Load book data first
    apiCall(`/api/books/${bookId}`).then(data => {
        const book = data.book;
        document.getElementById('update-book-id').value = book.book_id;
        document.getElementById('update-book-isbn').value = book.isbn || '';
        document.getElementById('update-book-title').value = book.title || '';
        document.getElementById('update-book-publisher').value = book.publisher || '';
        document.getElementById('update-book-year').value = book.published_year || '';
        document.getElementById('update-book-description').value = book.description || '';
        document.getElementById('update-book-form').style.display = 'block';
        document.getElementById('create-book-form').style.display = 'none';
    }).catch(error => {
        showError(error.message);
    });
}

function hideUpdateBookForm() {
    document.getElementById('update-book-form').style.display = 'none';
}

async function updateBook() {
    try {
        const auth = requireAuth();
        const bookId = document.getElementById('update-book-id').value;
        
        const bookData = {
            isbn: document.getElementById('update-book-isbn').value.trim() || null,
            title: document.getElementById('update-book-title').value.trim() || null,
            publisher: document.getElementById('update-book-publisher').value.trim() || null,
            published_year: document.getElementById('update-book-year').value ? parseInt(document.getElementById('update-book-year').value) : null,
            description: document.getElementById('update-book-description').value.trim() || null
        };
        
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        const data = await apiCall(`/api/books/${bookId}?${params.toString()}`, {
            method: 'PUT',
            body: JSON.stringify(bookData),
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Book updated successfully!');
        hideUpdateBookForm();
        getAllBooks();
    } catch (error) {
        showError(error.message);
    }
}

async function deleteBook(bookId) {
    if (!confirm('Are you sure you want to delete this book?')) {
        return;
    }
    
    try {
        const auth = requireAuth();
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        await apiCall(`/api/books/${bookId}?${params.toString()}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Book deleted successfully!');
        getAllBooks();
    } catch (error) {
        showError(error.message);
    }
}

function showSearchBooks() {
    document.getElementById('search-books-form').style.display = 'block';
}

function hideSearchBooks() {
    document.getElementById('search-books-form').style.display = 'none';
    document.getElementById('search-isbn').value = '';
    document.getElementById('search-title').value = '';
    document.getElementById('search-author').value = '';
    document.getElementById('search-category').value = '';
}

// Members Functions
async function getAllMembers() {
    try {
        const data = await apiCall('/api/members');
        displayMembers(data.members || []);
    } catch (error) {
        showError(error.message);
    }
}

function displayMembers(members) {
    const resultsDiv = document.getElementById('members-results');
    
    if (members.length === 0) {
        resultsDiv.innerHTML = '<div class="empty-state"><p>No members found</p></div>';
        return;
    }
    
    const isAdmin = currentUser && (currentUser.role === 'librarian' || currentUser.role === 'administrator');
    
    resultsDiv.innerHTML = '<div class="result-grid">' + members.map(member => `
        <div class="result-card">
            <h3>${member.name || 'Unnamed Member'}</h3>
            <p><strong>ID:</strong> ${member.member_id || 'N/A'}</p>
            <p><strong>Email:</strong> ${member.email || 'N/A'}</p>
            <p><strong>Phone:</strong> ${member.phone || 'N/A'}</p>
            <p><strong>Status:</strong> 
                <span class="badge badge-${getStatusClass(member.status)}">${member.status || 'N/A'}</span>
            </p>
            <p><strong>Join Date:</strong> ${member.join_date || 'N/A'}</p>
            ${isAdmin ? `
            <div class="action-buttons">
                <button onclick="showUpdateMemberForm(${member.member_id})" class="btn btn-secondary">Update</button>
                <button onclick="suspendMember(${member.member_id})" class="btn btn-warning">Suspend</button>
                <button onclick="deleteMember(${member.member_id})" class="btn btn-warning">Delete</button>
            </div>
            ` : ''}
        </div>
    `).join('') + '</div>';
}

function getStatusClass(status) {
    if (!status) return 'inactive';
    const statusLower = status.toLowerCase();
    if (statusLower === 'active') return 'active';
    if (statusLower === 'suspended') return 'suspended';
    return 'inactive';
}

function showRegisterMemberForm() {
    document.getElementById('register-member-form').style.display = 'block';
    document.getElementById('update-member-form').style.display = 'none';
}

function hideRegisterMemberForm() {
    document.getElementById('register-member-form').style.display = 'none';
    document.getElementById('member-name').value = '';
    document.getElementById('member-email').value = '';
    document.getElementById('member-phone').value = '';
}

async function registerMember() {
    try {
        const auth = requireAuth();
        const memberData = {
            name: document.getElementById('member-name').value.trim(),
            email: document.getElementById('member-email').value.trim(),
            phone: document.getElementById('member-phone').value.trim() || null
        };
        
        if (!memberData.name || !memberData.email) {
            showError('Name and Email are required');
            return;
        }
        
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        const data = await apiCall(`/api/members?${params.toString()}`, {
            method: 'POST',
            body: JSON.stringify(memberData),
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Member registered successfully!');
        hideRegisterMemberForm();
        getAllMembers();
    } catch (error) {
        showError(error.message);
    }
}

function showUpdateMemberForm(memberId) {
    apiCall(`/api/members/${memberId}`).then(data => {
        const member = data.member;
        document.getElementById('update-member-id').value = member.member_id;
        document.getElementById('update-member-name').value = member.name || '';
        document.getElementById('update-member-email').value = member.email || '';
        document.getElementById('update-member-phone').value = member.phone || '';
        document.getElementById('update-member-form').style.display = 'block';
        document.getElementById('register-member-form').style.display = 'none';
    }).catch(error => {
        showError(error.message);
    });
}

function hideUpdateMemberForm() {
    document.getElementById('update-member-form').style.display = 'none';
}

async function updateMember() {
    try {
        const auth = requireAuth();
        const memberId = document.getElementById('update-member-id').value;
        
        const memberData = {
            name: document.getElementById('update-member-name').value.trim() || null,
            email: document.getElementById('update-member-email').value.trim() || null,
            phone: document.getElementById('update-member-phone').value.trim() || null
        };
        
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        const data = await apiCall(`/api/members/${memberId}?${params.toString()}`, {
            method: 'PUT',
            body: JSON.stringify(memberData),
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Member updated successfully!');
        hideUpdateMemberForm();
        getAllMembers();
    } catch (error) {
        showError(error.message);
    }
}

async function suspendMember(memberId) {
    if (!confirm('Are you sure you want to suspend this member?')) {
        return;
    }
    
    try {
        const auth = requireAuth();
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        await apiCall(`/api/members/${memberId}/suspend?${params.toString()}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Member suspended successfully!');
        getAllMembers();
    } catch (error) {
        showError(error.message);
    }
}

async function deleteMember(memberId) {
    if (!confirm('Are you sure you want to delete this member?')) {
        return;
    }
    
    try {
        const auth = requireAuth();
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        await apiCall(`/api/members/${memberId}?${params.toString()}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Member deleted successfully!');
        getAllMembers();
    } catch (error) {
        showError(error.message);
    }
}

// Loans Functions
async function getAllLoans() {
    try {
        const data = await apiCall('/api/loans');
        displayLoans(data.loans || []);
    } catch (error) {
        showError(error.message);
    }
}

async function getActiveLoans() {
    try {
        const data = await apiCall('/api/loans/active');
        displayLoans(data.loans || []);
    } catch (error) {
        showError(error.message);
    }
}

async function getOverdueLoans() {
    try {
        const data = await apiCall('/api/loans/overdue');
        displayLoans(data.loans || []);
    } catch (error) {
        showError(error.message);
    }
}

function displayLoans(loans) {
    const resultsDiv = document.getElementById('loans-results');
    
    if (loans.length === 0) {
        resultsDiv.innerHTML = '<div class="empty-state"><p>No loans found</p></div>';
        return;
    }
    
    resultsDiv.innerHTML = '<div class="result-grid">' + loans.map(loan => `
        <div class="result-card">
            <h3>Loan #${loan.loan_id || 'N/A'}</h3>
            <p><strong>Member ID:</strong> ${loan.member_id || 'N/A'}</p>
            <p><strong>Copy ID:</strong> ${loan.copy_id || 'N/A'}</p>
            <p><strong>Librarian ID:</strong> ${loan.librarian_id || 'N/A'}</p>
            <p><strong>Issue Date:</strong> ${loan.issue_date || 'N/A'}</p>
            <p><strong>Due Date:</strong> ${loan.due_date || 'N/A'}</p>
            <p><strong>Return Date:</strong> ${loan.return_date || 'Not returned'}</p>
            <p><strong>Status:</strong> 
                <span class="badge badge-${getLoanStatusClass(loan.status)}">${loan.status || 'N/A'}</span>
            </p>
        </div>
    `).join('') + '</div>';
}

function getLoanStatusClass(status) {
    if (!status) return 'returned';
    const statusLower = status.toLowerCase();
    if (statusLower === 'active') return 'active';
    if (statusLower === 'overdue') return 'overdue';
    if (statusLower === 'returned') return 'returned';
    return 'returned';
}

function showIssueBookForm() {
    document.getElementById('issue-book-form').style.display = 'block';
    document.getElementById('return-book-form').style.display = 'none';
}

function hideIssueBookForm() {
    document.getElementById('issue-book-form').style.display = 'none';
    document.getElementById('issue-member-id').value = '';
    document.getElementById('issue-book-id').value = '';
    document.getElementById('issue-days').value = '14';
}

async function issueBook() {
    try {
        const auth = requireAuth();
        const loanData = {
            member_id: parseInt(document.getElementById('issue-member-id').value),
            book_id: parseInt(document.getElementById('issue-book-id').value),
            days: parseInt(document.getElementById('issue-days').value) || 14
        };
        
        if (!loanData.member_id || !loanData.book_id) {
            showError('Member ID and Book ID are required');
            return;
        }
        
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        const data = await apiCall(`/api/loans/issue?${params.toString()}`, {
            method: 'POST',
            body: JSON.stringify(loanData),
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Book issued successfully!');
        hideIssueBookForm();
        getAllLoans();
    } catch (error) {
        showError(error.message);
    }
}

function showReturnBookForm() {
    document.getElementById('return-book-form').style.display = 'block';
    document.getElementById('issue-book-form').style.display = 'none';
}

function hideReturnBookForm() {
    document.getElementById('return-book-form').style.display = 'none';
    document.getElementById('return-loan-id').value = '';
}

async function returnBook() {
    try {
        const auth = requireAuth();
        const loanData = {
            loan_id: parseInt(document.getElementById('return-loan-id').value)
        };
        
        if (!loanData.loan_id) {
            showError('Loan ID is required');
            return;
        }
        
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        await apiCall(`/api/loans/return?${params.toString()}`, {
            method: 'POST',
            body: JSON.stringify(loanData),
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess('Book returned successfully!');
        hideReturnBookForm();
        getAllLoans();
    } catch (error) {
        showError(error.message);
    }
}

async function updateOverdueLoans() {
    try {
        const auth = requireAuth();
        const params = new URLSearchParams({ email: auth.email, password: auth.password });
        const data = await apiCall(`/api/loans/update-overdue?${params.toString()}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        showSuccess(data.message || 'Overdue loans updated successfully!');
        getAllLoans();
    } catch (error) {
        showError(error.message);
    }
}

// Reservations Functions
async function getAllReservations() {
    try {
        const data = await apiCall('/api/reservations');
        displayReservations(data.reservations || []);
    } catch (error) {
        showError(error.message);
    }
}

function displayReservations(reservations) {
    const resultsDiv = document.getElementById('reservations-results');
    
    if (reservations.length === 0) {
        resultsDiv.innerHTML = '<div class="empty-state"><p>No reservations found</p></div>';
        return;
    }
    
    resultsDiv.innerHTML = '<div class="result-grid">' + reservations.map(reservation => `
        <div class="result-card">
            <h3>Reservation #${reservation.reservation_id || 'N/A'}</h3>
            <p><strong>Member ID:</strong> ${reservation.member_id || 'N/A'}</p>
            <p><strong>Book ID:</strong> ${reservation.book_id || 'N/A'}</p>
            <p><strong>Created At:</strong> ${reservation.created_at || 'N/A'}</p>
            <p><strong>Expires At:</strong> ${reservation.expires_at || 'N/A'}</p>
            <p><strong>Active:</strong> ${reservation.active ? 'Yes' : 'No'}</p>
            ${reservation.active ? `
            <div class="action-buttons">
                <button onclick="cancelReservation(${reservation.reservation_id})" class="btn btn-warning">Cancel</button>
            </div>
            ` : ''}
        </div>
    `).join('') + '</div>';
}

function showCreateReservationForm() {
    document.getElementById('create-reservation-form').style.display = 'block';
}

function hideCreateReservationForm() {
    document.getElementById('create-reservation-form').style.display = 'none';
    document.getElementById('reservation-member-id').value = '';
    document.getElementById('reservation-book-id').value = '';
    document.getElementById('reservation-days').value = '14';
}

async function createReservation() {
    try {
        const reservationData = {
            member_id: parseInt(document.getElementById('reservation-member-id').value),
            book_id: parseInt(document.getElementById('reservation-book-id').value),
            days_valid: parseInt(document.getElementById('reservation-days').value) || 14
        };
        
        if (!reservationData.member_id || !reservationData.book_id) {
            showError('Member ID and Book ID are required');
            return;
        }
        
        const data = await apiCall('/api/reservations', {
            method: 'POST',
            body: JSON.stringify(reservationData)
        });
        
        showSuccess('Reservation created successfully!');
        hideCreateReservationForm();
        getAllReservations();
    } catch (error) {
        showError(error.message);
    }
}

async function cancelReservation(reservationId) {
    if (!confirm('Are you sure you want to cancel this reservation?')) {
        return;
    }
    
    try {
        await apiCall(`/api/reservations/${reservationId}/cancel`, {
            method: 'POST'
        });
        
        showSuccess('Reservation cancelled successfully!');
        getAllReservations();
    } catch (error) {
        showError(error.message);
    }
}

// Initialize - check API health on load
window.addEventListener('DOMContentLoaded', async () => {
    try {
        await apiCall('/api/health');
    } catch (error) {
        showError('Cannot connect to API server. Make sure the server is running on ' + API_BASE_URL);
    }
});
