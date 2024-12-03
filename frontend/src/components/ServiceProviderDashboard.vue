<template>
  <div class="service-provider-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h2>Welcome, {{ userProfile.name || 'Professional' }}!</h2>
          <p class="header-subtitle">Manage your services and accept new requests</p>
        </div>
        <div class="header-right">
          <div class="header-actions">
            <button @click="showProfile" class="header-btn">
              <i class="fas fa-user"></i> Profile
            </button>
            <button @click="handleLogout" class="header-btn">
              <i class="fas fa-sign-out-alt"></i> Logout
            </button>
          </div>
          <div v-if="averageRating > 0" class="rating-display">
            <span class="rating-label">Your Rating:</span>
            <div class="rating-stars">
              <i class="fas fa-star" v-for="n in Math.floor(averageRating)" :key="n"></i>
              <i class="fas fa-star-half-alt" v-if="averageRating % 1 >= 0.5"></i>
              <span class="rating-value">{{ averageRating.toFixed(1) }}/5</span>
              <span class="rating-count">({{ totalRatings }} ratings)</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 1. Requested Services Section -->
    <section class="requested-services">
      <h3>Requested Services</h3>
      <div class="requests-container">
        <div v-if="requestedServices.length === 0" class="no-requests">
          No service requests available at the moment.
        </div>
        <div v-else class="requests-grid">
          <div v-for="request in requestedServices" :key="request.id" class="request-card requested">
            <div class="request-header">
              <span class="request-id">Request #{{ request.id }}</span>
              <span class="status-badge status-requested">
                <i class="fas fa-clock"></i> Requested
              </span>
            </div>
            
            <div class="request-details">
              <div class="service-info">
                <h4>{{ request.service_name }}</h4>
                <span class="price">₹{{ request.price }}</span>
              </div>
              
              <div class="customer-info">
                <p><i class="fas fa-user"></i> {{ request.customer_name }}</p>
                <p><i class="fas fa-map-marker-alt"></i> {{ request.address }}</p>
                <p><i class="fas fa-calendar"></i> Requested on: {{ formatDate(request.date_of_request) }}</p>
              </div>
              
              <div class="request-notes" v-if="request.remarks">
                <h5>Customer Notes:</h5>
                <p class="remarks">{{ request.remarks }}</p>
              </div>
            </div>

            <div class="request-actions">
              <button @click="acceptRequest(request.id)" class="btn-accept">
                <i class="fas fa-check"></i> Accept Request
              </button>
              <button @click="rejectRequest(request.id)" class="btn-reject">
                <i class="fas fa-times"></i> Reject Request
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Accepted Services Section -->
    <section class="accepted-services">
      <h3>Accepted Services</h3>
      <div class="requests-container">
        <div v-if="acceptedRequests.length === 0" class="no-requests">
          No accepted services yet.
        </div>
        <div v-else class="requests-grid">
          <div v-for="request in acceptedRequests" :key="request.id" class="request-card accepted">
            <div class="request-header">
              <span class="request-id">Request #{{ request.id }}</span>
              <span class="status-accepted">Accepted</span>
            </div>
            <div class="request-details">
              <p><strong>Service:</strong> {{ request.service_name }}</p>
              <p><strong>Price:</strong> ₹{{ request.price }}</p>
              <p><strong>Customer:</strong> {{ request.customer_name }}</p>
              <p><strong>Address:</strong> {{ request.address }}</p>
              <p><strong>Date Requested:</strong> {{ formatDate(request.date_of_request) }}</p>
              <p v-if="request.remarks"><strong>Notes:</strong> {{ request.remarks }}</p>
            </div>
            <div class="status-message">
              You have accepted this request
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Completed Services Section -->
    <section class="completed-services">
      <h3>Completed & Rejected Services</h3>
      <div class="requests-container">
        <div v-if="completedAndRejectedRequests.length === 0" class="no-requests">
          No completed or rejected services yet.
        </div>
        <template v-else>
          <!-- Group completed and rejected requests into rows of 3 -->
          <div class="row" v-for="(group, index) in groupedCompletedAndRejectedRequests" :key="index">
            <div v-for="request in group" :key="request.id" 
                 :class="['request-card', request.status === 'rejected' ? 'rejected' : 'completed']">
              <div class="request-header">
                <div class="header-content">
                  <span class="request-id">Request #{{ request.id }}</span>
                  <span :class="['status-badge', request.status === 'rejected' ? 'status-rejected' : 'status-completed']">
                    <i :class="request.status === 'rejected' ? 'fas fa-times-circle' : 'fas fa-check-circle'"></i>
                    {{ request.status === 'rejected' ? 'Rejected' : 'Completed' }}
                  </span>
                </div>
                <div class="completion-date">
                  {{ formatDate(request.date_of_completion || request.date_of_request) }}
                </div>
              </div>
              <div class="request-details">
                <div class="service-info">
                  <h4>{{ request.service_name }}</h4>
                  <span class="price">₹{{ request.price }}</span>
                </div>
                <div class="customer-info">
                  <p><i class="fas fa-user"></i> {{ request.customer_name }}</p>
                  <p><i class="fas fa-map-marker-alt"></i> {{ request.address }}</p>
                </div>
                <div class="completion-info" v-if="request.remarks">
                  <h5>Notes:</h5>
                  <p class="remarks">{{ request.remarks }}</p>
                </div>
                <div class="rating-info" v-if="request.status === 'completed'">
                  <div class="rating" v-if="request.rating">
                    <span class="rating-label">Customer Rating:</span>
                    <div class="stars">
                      <i class="fas fa-star" v-for="n in request.rating" :key="n"></i>
                      <span class="rating-number">{{ request.rating }}/5</span>
                    </div>
                    <p class="rating-date">Rated on: {{ formatDate(request.date_of_completion) }}</p>
                  </div>
                  <div class="no-rating" v-else>
                    No rating provided
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </section>

    <!-- Add Profile Modal -->
    <div v-if="showProfileModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Professional Profile</h3>
          <button class="close-btn" @click="closeProfile">&times;</button>
        </div>
        <div class="profile-content">
          <div v-if="!isEditing">
            <div class="profile-info">
              <div class="rating-section">
                <h4>Rating Overview</h4>
                <div class="rating-stats">
                  <div class="average-rating">
                    <span class="rating-number">{{ userProfile.average_rating }}</span>
                    <div class="stars">
                      <i class="fas fa-star" v-for="n in Math.floor(userProfile.average_rating)" :key="n"></i>
                      <i class="fas fa-star-half-alt" v-if="userProfile.average_rating % 1 >= 0.5"></i>
                    </div>
                    <span class="total-ratings">({{ userProfile.total_ratings }} ratings)</span>
                  </div>
                </div>
                
                <!-- Recent Ratings -->
                <div class="recent-ratings" v-if="userProfile.recent_ratings && userProfile.recent_ratings.length > 0">
                  <h5>Recent Ratings</h5>
                  <div class="rating-item" v-for="(rating, index) in userProfile.recent_ratings" :key="index">
                    <div class="rating-stars">
                      <i class="fas fa-star" v-for="n in rating.rating" :key="n"></i>
                    </div>
                    <div class="rating-details">
                      <p class="rating-comment" v-if="rating.comment">{{ rating.comment }}</p>
                      <span class="rating-date">{{ formatDate(rating.date) }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Rest of profile info -->
              <p><strong>Name:</strong> {{ userProfile.name }}</p>
              <p><strong>Email:</strong> {{ userProfile.email }}</p>
              <p><strong>Service:</strong> {{ userProfile.service_name }}</p>
              <p><strong>Experience:</strong> {{ userProfile.experience_years }} years</p>
              <p><strong>Address:</strong> {{ userProfile.address }}</p>
              <p><strong>Pin Code:</strong> {{ userProfile.pin_code }}</p>
            </div>
            <button @click="startEditing" class="btn-edit-profile">Edit Profile</button>
          </div>
          <div v-else class="edit-profile-form">
            <form @submit.prevent="updateProfile">
              <div class="form-group">
                <label>Name</label>
                <input type="text" v-model="editedProfile.name" class="form-control" required>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="editedProfile.email" class="form-control" required>
              </div>
              <div class="form-group">
                <label>Service</label>
                <input type="text" v-model="editedProfile.service_name" class="form-control" required>
              </div>
              <div class="form-group">
                <label>Experience (Years)</label>
                <input type="number" v-model="editedProfile.experience_years" class="form-control" required>
              </div>
              <div class="form-group">
                <label>Address</label>
                <textarea v-model="editedProfile.address" class="form-control" required></textarea>
              </div>
              <div class="form-group">
                <label>Pin Code</label>
                <input type="text" v-model="editedProfile.pin_code" class="form-control" required>
              </div>
              <div class="form-actions">
                <button type="submit" class="btn-save">Save Changes</button>
                <button type="button" @click="cancelEdit" class="btn-cancel">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      serviceRequests: [],
      showProfileModal: false,
      isEditing: false,
      userProfile: {
        name: '',
        email: '',
        service_name: '',
        experience_years: '',
        address: '',
        pin_code: ''
      },
      editedProfile: {
        name: '',
        email: '',
        service_name: '',
        experience_years: '',
        address: '',
        pin_code: ''
      },
      averageRating: 0,
      totalRatings: 0,
    };
  },
  computed: {
    newRequests() {
      return this.serviceRequests.filter(req => req.status === 'requested');
    },
    acceptedRequests() {
      return this.serviceRequests.filter(req => req.status === 'accepted');
    },
    completedAndRejectedRequests() {
      return this.serviceRequests.filter(req => 
        req.status === 'completed' || req.status === 'rejected'
      );
    },
    groupedCompletedAndRejectedRequests() {
      const result = [];
      const itemsPerRow = 3;
      const requests = this.completedAndRejectedRequests;
      
      for (let i = 0; i < requests.length; i += itemsPerRow) {
        result.push(requests.slice(i, i + itemsPerRow));
      }
      return result;
    },
    requestedServices() {
      return this.serviceRequests.filter(req => req.status === 'requested');
    }
  },
  created() {
    this.fetchServiceRequests();
    this.fetchProfessionalProfile();
    this.calculateRatings();
  },
  methods: {
    async fetchServiceRequests() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          console.error('No token found');
          this.$router.push('/login');
          return;
        }

        console.log('Fetching requests with token:', token);
        const response = await axios.get('http://127.0.0.1:5000/professional/service-requests', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        console.log('Service requests response:', response.data);
        this.serviceRequests = response.data.requests;
        this.calculateRatings();
        
        // Add debug logging for rejected services
        const rejected = this.serviceRequests.filter(req => req.status === 'rejected');
        console.log('Rejected requests:', rejected);
      } catch (error) {
        console.error('Error fetching service requests:', error);
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('userRole');
          this.$router.push('/login');
        }
      }
    },

    async fetchProfessionalProfile() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          console.error('No token found');
          this.$router.push('/login');
          return;
        }

        console.log('Fetching profile with token:', token);
        const response = await axios.get('http://127.0.0.1:5000/professional/profile', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        console.log('Profile response:', response.data);
        this.userProfile = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('userRole');
          this.$router.push('/login');
        }
      }
    },

    showProfile() {
      this.showProfileModal = true;
      this.fetchProfessionalProfile();
    },

    closeProfile() {
      this.showProfileModal = false;
      this.isEditing = false;
    },

    startEditing() {
      this.editedProfile = { ...this.userProfile };
      this.isEditing = true;
    },

    cancelEdit() {
      this.isEditing = false;
      this.editedProfile = { ...this.userProfile };
    },

    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        await axios.put('http://127.0.0.1:5000/professional/profile', this.editedProfile, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.userProfile = { ...this.editedProfile };
        this.isEditing = false;
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Error updating profile');
      }
    },

    async acceptRequest(requestId) {
      try {
        const token = localStorage.getItem('token');
        await axios.post(`http://127.0.0.1:5000/professional/service-request/${requestId}/accept`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        alert('Service request accepted successfully');
        await this.fetchServiceRequests();
      } catch (error) {
        console.error('Error accepting request:', error);
        alert('Error accepting request');
      }
    },

    async rejectRequest(requestId) {
      try {
        const token = localStorage.getItem('token');
        await axios.post(`http://127.0.0.1:5000/professional/service-request/${requestId}/reject`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        alert('Service request rejected');
        await this.fetchServiceRequests();
      } catch (error) {
        console.error('Error rejecting request:', error);
        alert('Error rejecting request');
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },

    async handleLogout() {
      try {
        const token = localStorage.getItem('token');
        await axios.get('http://127.0.0.1:5000/logout', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        localStorage.removeItem('token');
        localStorage.removeItem('userRole');
        this.$router.push('/login');
      } catch (error) {
        console.error('Logout error:', error);
        // Even if the server request fails, clear local storage and redirect
        localStorage.clear();
        this.$router.push('/login');
      }
    },

    calculateRatings() {
      const completedServices = this.serviceRequests.filter(req => 
        req.status === 'completed' && req.rating
      );
      
      if (completedServices.length > 0) {
        const totalRating = completedServices.reduce((sum, req) => sum + req.rating, 0);
        this.averageRating = totalRating / completedServices.length;
        this.totalRatings = completedServices.length;
      }
    },
  }
};
</script>

<style scoped>
.service-provider-dashboard {
  padding-top: 120px;
  background-color: #1a1a1a;
  color: #fff;
  padding: 20px;
}

.dashboard-header {
  background: #242424;
  padding: 15px 0 0 0;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.header-content {
  padding: 0 30px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 1400px;
  margin: 0 auto;
}

.header-title {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.header-title h2 {
  color: #4CAF50;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.header-subtitle {
  color: #888;
  font-size: 14px;
  margin: 0;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.header-actions {
  display: flex;
  gap: 15px;
}

.header-btn {
  background: transparent;
  border: 1px solid #4CAF50;
  color: #4CAF50;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.header-btn:hover {
  background: #4CAF50;
  color: white;
}

.rating-display {
  background: rgba(255, 255, 255, 0.05);
  padding: 8px 15px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-label {
  color: #888;
  font-size: 0.9em;
}

.rating-stars {
  display: flex;
  align-items: center;
  gap: 5px;
}

.rating-stars i {
  color: #ffc107;
}

.rating-value {
  color: #ffc107;
  font-weight: bold;
  margin-left: 5px;
}

.rating-count {
  color: #888;
  font-size: 0.9em;
}

section {
  background: #242424;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

section h3 {
  color: #4CAF50;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #444;
}

.requests-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.request-card {
  background: #2d2d2d;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  padding: 20px;
  transition: transform 0.3s ease;
}

.request-card:hover {
  transform: translateY(-5px);
}

.request-card.accepted {
  border-left: 4px solid #28a745;
}

.request-card.completed {
  border-left: 4px solid #17a2b8;
}

.request-card.rejected {
  border-left: 4px solid #dc3545;
}

.request-details {
  color: #ddd;
  margin: 15px 0;
}

.request-details p {
  margin: 8px 0;
}

.request-details strong {
  color: #fff;
}

.price {
  color: #4CAF50;
  font-weight: bold;
}

.request-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #444;
}

.btn-accept {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  flex: 1;
  transition: all 0.3s ease;
}

.btn-reject {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  flex: 1;
  transition: all 0.3s ease;
}

.btn-accept:hover, .btn-reject:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: bold;
  margin-top: 10px;
}

.status-requested {
  background-color: #ffc107;
  color: black;
}

.status-accepted {
  background-color: #28a745;
  color: white;
}

.status-completed {
  background-color: #17a2b8;
  color: white;
}

.status-rejected {
  background-color: #dc3545;
  color: white;
}

.no-requests {
  text-align: center;
  padding: 20px;
  color: #888;
  background: #2d2d2d;
  border-radius: 8px;
  grid-column: 1 / -1;
}

/* Profile Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #2d2d2d;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #444;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #fff;
  cursor: pointer;
}

.profile-content {
  padding: 20px;
}

.profile-info p {
  margin: 10px 0;
  font-size: 1.1em;
  color: #ddd;
}

.btn-edit-profile {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  margin-top: 20px;
  cursor: pointer;
  width: 100%;
  transition: all 0.3s ease;
}

.btn-edit-profile:hover {
  background-color: #45a049;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #fff;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 4px;
  background: #333;
  color: #fff;
}

.form-control:focus {
  outline: none;
  border-color: #4CAF50;
}

.btn-profile {
  background: linear-gradient(45deg, #9b59b6, #8e44ad);
  box-shadow: 0 4px 15px rgba(155, 89, 182, 0.3);
}

.btn-profile:hover {
  background: linear-gradient(45deg, #8e44ad, #803d9f);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .requests-container {
    grid-template-columns: 1fr;
  }
  
  .request-actions {
    flex-direction: column;
  }
  
  .modal-content {
    width: 95%;
    margin: 10px;
  }
}

.completed-services .requests-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 10px;
}

.completed-services .row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.completed-services .request-card {
  flex: 1;
  min-width: 300px;
  max-width: calc(33.333% - 14px); /* For 3 cards per row */
  background: linear-gradient(145deg, #2d2d2d, #333);
  border-radius: 12px;
  overflow: hidden;
}

.completed-services .request-header {
  background: linear-gradient(90deg, #17a2b8, #20c997);
  padding: 15px 20px;
  color: white;
}

.completed-services .request-details {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.completed-services .request-id {
  font-weight: bold;
  font-size: 1.1em;
}

.completed-services .status-completed {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
}

.completed-services .status-completed i {
  font-size: 1.2em;
}

.completed-services .request-details {
  padding: 20px;
}

.completed-services .service-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.completed-services .service-info h4 {
  margin: 0;
  color: #fff;
  font-size: 1.2em;
}

.completed-services .price {
  font-size: 1.2em;
  font-weight: bold;
  color: #20c997;
}

.completed-services .customer-info {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.completed-services .customer-info p {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ddd;
}

.completed-services .customer-info i {
  color: #17a2b8;
}

.completed-services .completion-info {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.completed-services .completion-info h5 {
  color: #17a2b8;
  margin-bottom: 8px;
  font-size: 1em;
}

.completed-services .remarks {
  color: #bbb;
  font-style: italic;
  line-height: 1.4;
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 6px;
}

.completed-services .rating {
  margin-top: 15px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.completed-services .rating-label {
  display: block;
  margin-bottom: 5px;
  color: #17a2b8;
  font-weight: 500;
}

.completed-services .stars {
  display: flex;
  align-items: center;
  gap: 5px;
}

.completed-services .stars i {
  color: #ffc107;
}

.completed-services .rating-number {
  margin-left: 8px;
  color: #ffc107;
  font-weight: bold;
}

@media (max-width: 1400px) {
  .completed-services .request-card {
    flex: 0 0 calc(50% - 20px);
  }
}

@media (max-width: 768px) {
  .completed-services .request-card {
    flex: 0 0 100%;
  }
}

.request-card.rejected {
  border-left: 4px solid #dc3545;
}

.status-rejected {
  background-color: #dc3545;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-completed {
  background-color: #28a745;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.rating-summary {
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 15px;
  border-radius: 8px;
  margin-top: 10px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.rating-summary .rating-label {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.rating-summary .stars {
  display: flex;
  align-items: center;
  gap: 3px;
}

.rating-summary .stars i {
  color: #ffd700;
  font-size: 1.2em;
}

.rating-summary .rating-number {
  color: white;
  margin-left: 5px;
  font-weight: bold;
}

.rating-summary .total-ratings {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9em;
}

.rating-info {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
}

.rating-date {
  color: #888;
  font-size: 0.9em;
  margin-top: 5px;
}

.no-rating {
  color: #888;
  font-style: italic;
}

.rating-section {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.rating-stats {
  text-align: center;
  margin-bottom: 20px;
}

.average-rating {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.rating-number {
  font-size: 2em;
  font-weight: bold;
  color: #ffc107;
}

.stars {
  color: #ffc107;
  font-size: 1.2em;
}

.total-ratings {
  color: #888;
  font-size: 0.9em;
}

.recent-ratings {
  margin-top: 20px;
}

.rating-item {
  padding: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.rating-item:last-child {
  border-bottom: none;
}

.rating-stars {
  color: #ffc107;
  margin-bottom: 5px;
}

.rating-comment {
  color: #ddd;
  font-style: italic;
  margin: 5px 0;
}

.rating-date {
  color: #888;
  font-size: 0.8em;
}

.requested-services {
  margin-top: 20px;
  background: #242424;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
}

.requested-services h3 {
  color: #4CAF50;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #444;
}

.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.request-card.requested {
  background: #2d2d2d;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.request-card.requested:hover {
  transform: translateY(-5px);
}

.request-header {
  background: linear-gradient(90deg, #ffc107, #ff9800);
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.request-id {
  font-weight: bold;
  color: #fff;
}

.status-badge.status-requested {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(0, 0, 0, 0.2);
  padding: 5px 10px;
  border-radius: 20px;
  color: #fff;
}

.request-details {
  padding: 20px;
}

.service-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.service-info h4 {
  margin: 0;
  color: #fff;
  font-size: 1.2em;
}

.price {
  font-size: 1.2em;
  font-weight: bold;
  color: #4CAF50;
}

.customer-info {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.customer-info p {
  margin: 8px 0;
  color: #ddd;
  display: flex;
  align-items: center;
  gap: 10px;
}

.customer-info i {
  color: #4CAF50;
  width: 20px;
  text-align: center;
}

.request-notes {
  margin-top: 15px;
}

.request-notes h5 {
  color: #4CAF50;
  margin-bottom: 8px;
}

.remarks {
  color: #bbb;
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 6px;
  font-style: italic;
}

.request-actions {
  padding: 15px;
  display: flex;
  gap: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-accept, .btn-reject {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-accept {
  background: #4CAF50;
  color: white;
}

.btn-reject {
  background: #dc3545;
  color: white;
}

.btn-accept:hover, .btn-reject:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
}

.no-requests {
  text-align: center;
  padding: 30px;
  color: #888;
  font-style: italic;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.header-left {
  display: flex;
  flex-direction: column;
}
</style>
