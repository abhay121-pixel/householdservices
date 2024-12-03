<template>
  <div class="signup-container">
    <div class="header">
      <button @click="goToHome" class="home-btn">
        <i class="fas fa-home"></i> Home
      </button>
      <h1>Household Services</h1>
    </div>
    <div class="signup-content">
      <div class="image-section">
        <div class="overlay"></div>
        <h1>Join Our Professional Network</h1>
        <p>Register as a service provider and start offering your services</p>
      </div>
      
      <div class="form-section">
        <div class="form-container">
          <h2>Professional Registration</h2>
          <p class="subtitle">Please fill in your details</p>
          
          <form @submit.prevent="register">
            <div class="form-group">
              <label for="username">Username</label>
              <input type="text" id="username" v-model="username" required />
            </div>

            <div class="form-group">
              <label for="name">Full Name</label>
              <input type="text" id="name" v-model="name" required />
            </div>

            <div class="form-group">
              <label for="email">Email</label>
              <input type="email" id="email" v-model="email" required />
            </div>

            <div class="form-group">
              <label for="service_name">Service Type</label>
              <input type="text" id="service_name" v-model="service_name" required />
            </div>

            <div class="form-group">
              <label for="experience_years">Years of Experience</label>
              <input type="number" id="experience_years" v-model="experience_years" required />
            </div>

            <div class="form-group">
              <label for="address">Address</label>
              <textarea id="address" v-model="address" required></textarea>
            </div>

            <div class="form-group">
              <label for="pin_code">Pin Code</label>
              <input type="text" id="pin_code" v-model="pin_code" required />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input type="password" id="password" v-model="password" required />
            </div>

            <div class="form-group">
              <label for="confirmPassword">Confirm Password</label>
              <input type="password" id="confirmPassword" v-model="confirmPassword" required />
            </div>

            <div class="form-group">
              <label for="document">Upload Document (PDF/Image)</label>
              <div class="upload-container">
                <input 
                  type="file" 
                  id="document" 
                  @change="handleFileUpload" 
                  accept=".pdf,.jpg,.jpeg,.png"
                  class="file-input"
                />
                <div class="upload-button">
                  <i class="fas fa-upload"></i>
                  Choose File
                </div>
                <span class="file-name" v-if="document">{{ document.name }}</span>
                <span class="file-hint" v-else>Supported formats: PDF, JPG, PNG</span>
              </div>
            </div>

            <div v-if="document && isImage" class="image-preview">
              <img :src="previewUrl" alt="Document preview" />
            </div>

            <button type="submit" class="signup-btn">Register</button>
            <button type="button" class="login-link" @click="goToLogin">
              Already have an account? Login
            </button>

            <div v-if="message" :class="['message', messageClass]">
              {{ message }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.signup-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1a1a1a;
  padding: 20px;
  padding-top: 80px;
}

.signup-content {
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
  background-image: url('https://images.unsplash.com/photo-1585128792020-803d29415281?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
  padding: 40px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  text-align: center;
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

input, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #444;
  border-radius: 8px;
  background: #333;
  color: #fff;
  font-size: 1em;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #4CAF50;
}

.signup-btn {
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

.signup-btn:hover {
  background: #45a049;
}

.login-link {
  width: 100%;
  padding: 12px;
  background: transparent;
  color: #4CAF50;
  border: 1px solid #4CAF50;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.login-link:hover {
  background: #4CAF50;
  color: white;
}

.message {
  padding: 12px;
  border-radius: 8px;
  margin-top: 20px;
}

.alert-success {
  background: #28a745;
  color: white;
}

.alert-danger {
  background: #dc3545;
  color: white;
}

@media (max-width: 768px) {
  .signup-content {
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

.upload-container {
  position: relative;
  margin-top: 10px;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 2;
}

.upload-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background: #45a049;
}

.file-name {
  margin-left: 10px;
  color: #4CAF50;
  font-weight: 500;
}

.file-hint {
  margin-left: 10px;
  color: #666;
  font-size: 0.9em;
}

.image-preview {
  margin-top: 15px;
  max-width: 300px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.image-preview img {
  width: 100%;
  height: auto;
  display: block;
}

.upload-container {
  border: 2px dashed #444;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  background: rgba(255, 255, 255, 0.05);
  transition: border-color 0.3s;
}

.upload-container:hover {
  border-color: #4CAF50;
}

.upload-button i {
  font-size: 1.2em;
}

.file-error {
  color: #dc3545;
  margin-top: 5px;
  font-size: 0.9em;
}
</style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      service_name: "",
      experience_years: "",
      address: "",
      pin_code: "",
      document: null,
      previewUrl: null,
      isImage: false,
      message: "",
      messageClass: "",
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          alert('File size should not exceed 5MB');
          event.target.value = '';
          return;
        }

        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
        if (!allowedTypes.includes(file.type)) {
          alert('Please upload a PDF or image file (JPG, PNG)');
          event.target.value = '';
          return;
        }

        this.document = file;
        this.isImage = file.type.startsWith('image/');

        if (this.isImage) {
          this.previewUrl = URL.createObjectURL(file);
        } else {
          this.previewUrl = null;
        }
      }
    },
    validateAddressAndPincode() {
      if (!this.address) {
        this.message = "Address is required.";
        this.messageClass = "alert alert-danger";
        return false;
      }
      if (!this.pin_code || !/^\d{5,6}$/.test(this.pin_code)) {
        this.message = "Please enter a valid pincode (5-6 digits).";
        this.messageClass = "alert alert-danger";
        return false;
      }
      return true;
    },
    register() {
      if (this.password !== this.confirmPassword) {
        this.message = "Passwords do not match.";
        this.messageClass = "alert alert-danger";
        return;
      }

      if (!this.document) {
        this.message = "Please upload a document";
        this.messageClass = "alert alert-danger";
        return;
      }

      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('password', this.password);
      formData.append('role', 'service_professional');
      formData.append('name', this.name);
      formData.append('email', this.email);
      formData.append('address', this.address);
      formData.append('pin_code', this.pin_code);
      formData.append('service_name', this.service_name);
      formData.append('experience_years', this.experience_years);

      if (this.document) {
        formData.append('document_upload', this.document);
      }

      console.log('Sending registration data:', {
        username: this.username,
        role: 'service_professional',
        name: this.name,
        email: this.email,
        address: this.address,
        pin_code: this.pin_code,
        service_name: this.service_name,
        experience_years: this.experience_years
      });

      axios.post('http://127.0.0.1:5000/signup', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        this.message = response.data.message;
        this.messageClass = "alert alert-success";
        setTimeout(() => this.$router.push('/login'), 2000);
      })
      .catch(error => {
        console.error('Registration error:', error.response?.data);
        this.message = error.response?.data?.message || 'Registration failed';
        this.messageClass = "alert alert-danger";
      });
    },
    goToLogin() {
      this.$router.push("/login");
    },
    goToHome() {
      this.$router.push('/login');
    }
  },
  beforeDestroy() {
    if (this.previewUrl) {
      URL.revokeObjectURL(this.previewUrl);
    }
  }
};
</script>
