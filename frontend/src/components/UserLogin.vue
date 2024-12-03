<template>
  <div class="login-container">
    <div class="header">
      <button @click="goToHome" class="home-btn">
        <i class="fas fa-home"></i> Home
      </button>
      <h1>Household Services</h1>
    </div>
    <div class="login-content">
      <div class="image-section">
        <div class="overlay"></div>
        <h1>Household Services</h1>
        <p>Your one-stop solution for all household services</p>
      </div>
      
      <div class="form-section">
        <div class="form-container">
          <h2>Welcome Back</h2>
          <p class="subtitle">Please login to continue</p>
          
          <form @submit.prevent="login">
            <div class="form-group">
              <label for="email">Email</label>
              <input
                type="email"
                id="email"
                v-model="email"
                placeholder="Enter your email"
              />
            </div>
            
            <div class="form-group">
              <label for="password">Password</label>
              <input
                type="password"
                id="password"
                v-model="password"
                placeholder="Enter your password"
              />
            </div>
            
            <div class="form-group">
              <label for="role">Login as:</label>
              <select
                id="role"
                v-model="role"
              >
                <option value="admin">Admin</option>
                <option value="customer">Customer</option>
                <option value="service_professional">Service Provider</option>
              </select>
            </div>

            <button type="submit" class="login-btn">Login</button>

            <div class="register-options">
              <button
                type="button"
                class="register-btn customer"
                @click="goToCustomerRegister"
              >
                Register as Customer
              </button>
              <button
                type="button"
                class="register-btn professional"
                @click="goToServiceProviderRegister"
              >
                Register as Professional
              </button>
            </div>

            <div v-if="message" :class="['message', messageClass]">
              {{ message }}
            </div>
            
            <div v-if="pendingApproval" class="pending-message">
              Your account is pending approval. Please wait for admin approval before logging in.
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1a1a1a;
  padding: 20px;
  padding-top: 80px;
}

.login-content {
  display: flex;
  width: 1000px;
  max-width: 95%;
  background: #242424;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

.image-section {
  flex: 1;
  position: relative;
  background-image: url('https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
  padding: 40px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7));
}

.image-section h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  position: relative;
  z-index: 1;
}

.image-section p {
  font-size: 1.2em;
  position: relative;
  z-index: 1;
}

.form-section {
  flex: 1;
  padding: 40px;
  background: #2d2d2d;
}

.form-container {
  max-width: 400px;
  margin: 0 auto;
}

h2 {
  color: #fff;
  margin-bottom: 10px;
  font-size: 2em;
}

.subtitle {
  color: #888;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  color: #fff;
  margin-bottom: 8px;
}

input, select {
  width: 100%;
  padding: 12px;
  border: 1px solid #444;
  border-radius: 8px;
  background: #333;
  color: #fff;
  font-size: 1em;
}

input:focus, select:focus {
  outline: none;
  border-color: #4CAF50;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background: #45a049;
}

.register-options {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.register-btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: opacity 0.3s;
}

.register-btn.customer {
  background: #2196F3;
}

.register-btn.professional {
  background: #9C27B0;
}

.register-btn:hover {
  opacity: 0.9;
}

.message {
  padding: 12px;
  border-radius: 8px;
  margin-top: 20px;
}

.alert-danger {
  background: #ff5252;
  color: white;
}

.alert-warning {
  background: #ffc107;
  color: black;
}

.pending-message {
  background: #ff9800;
  color: white;
  padding: 12px;
  border-radius: 8px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .login-content {
    flex-direction: column;
  }
  
  .image-section {
    padding: 60px 20px;
  }
  
  .form-section {
    padding: 30px 20px;
  }
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 15px 30px;
  background: #1a1a1a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
  z-index: 1000;
}

.header h1 {
  color: #4CAF50;
  margin: 0;
  font-size: 1.5em;
  font-weight: bold;
}

.home-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.home-btn:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}
</style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      role: "customer",
      message: "",
      messageClass: "",
      pendingApproval: false
    };
  },
  methods: {
    login() {
      this.pendingApproval = false;
      
      axios.post("http://127.0.0.1:5000/login", {
        email: this.email,
        password: this.password,
        role: this.role,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      })
      .then((response) => {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('userRole', response.data.role);
        
        if (response.data.role === 'admin') {
          this.$router.push('/admin');
        } else if (response.data.role === 'customer') {
          this.$router.push('/user');
        } else {
          this.$router.push('/serviceprovider');
        }
      })
      .catch((error) => {
        if (error.response?.status === 403 && 
            error.response?.data?.message?.includes('pending approval')) {
          this.pendingApproval = true;
          this.message = "Account pending approval";
          this.messageClass = "alert alert-warning";
        } else {
          this.message = error.response?.data?.message || "Login failed";
          this.messageClass = "alert alert-danger";
        }
      });
    },
    goToCustomerRegister() {
      // Redirect to the customer registration page
      this.$router.push("/signup");
    },
    goToServiceProviderRegister() {
      // Redirect to the service provider registration page
      this.$router.push("/signup/service-provider");
    },
    goToHome() {
      this.$router.push('/login');
    }
  },
  created() {
    // Clear any existing auth data when arriving at login page
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
  }
};
</script>
