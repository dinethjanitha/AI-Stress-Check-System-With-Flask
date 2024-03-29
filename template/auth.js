// Simulated user data (replace with actual implementation)
const users = [
    { username: 'user1', password: 'password1' },
    { username: 'user2', password: 'password2' },
    { username: 'user3', password: 'password3' }
  ];
  
  // Function to check if a user is authenticated
  function isAuthenticated() {
    const token = localStorage.getItem('token');
    return token !== null;
  }
  
  // Function to log in a user
  function login(username, password) {
    const user = users.find(u => u.username === username && u.password === password);
    
    if (user) {
      const token = generateToken();
      localStorage.setItem('token', token);
      return true;
    }
    
    return false;
  }
  
  // Function to log out a user
  function logout() {
    localStorage.removeItem('token');
  }
  
  // Function to generate a random token
  function generateToken() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let token = '';
    
    for (let i = 0; i < 10; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      token += characters.charAt(randomIndex);
    }
    
    return token;
  }
  
  // Usage example:
  // const loggedIn = login('user1', 'password1');
  // if (loggedIn) {
  //   // User is logged in
  // } else {
  //   // Invalid username or password
  // }
  
  