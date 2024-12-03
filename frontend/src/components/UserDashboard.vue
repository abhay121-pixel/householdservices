<template>
  <div class="user-dashboard">
    <!-- Header Section -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h2>Welcome, {{ userProfile.name || 'User' }}!</h2>
        </div>
        <div class="header-actions">
          <button @click="showProfile" class="header-btn">
            <i class="fas fa-user"></i> Profile
          </button>
          <button @click="handleLogout" class="header-btn">
            <i class="fas fa-sign-out-alt"></i> Logout
          </button>
        </div>
      </div>
    </header>

    <!-- Available Services Section -->
    <section class="dashboard-section">
      <h3>Available Services</h3>
      <div class="services-grid">
        <div v-for="service in services" :key="service.id" class="service-card">
          <div class="service-header">
            <h4>{{ service.name }}</h4>
            <span class="price">₹{{ service.price }}</span>
          </div>
          
          <div class="service-content">
            <p class="description">{{ service.description }}</p>
            <div class="service-meta">
              <span class="time-required">
                <i class="fas fa-clock"></i> {{ service.time_required }}
              </span>
            </div>
          </div>

          <button @click="requestService(service)" class="btn-request">
            <i class="fas fa-plus"></i> Request Service
          </button>
        </div>
      </div>
    </section>

    <!-- Requested Services Section -->
    <section class="dashboard-section">
      <h3>Requested Services</h3>
      <div class="requests-grid">
        <div v-for="request in requestedServices" :key="request.id" class="request-card requested">
          <div class="request-header">
            <span class="service-name">{{ request.service_name }}</span>
            <span class="status-badge status-requested">Requested</span>
          </div>
          <div class="request-details">
            <p><i class="fas fa-calendar"></i> Requested on: {{ formatDate(request.date_of_request) }}</p>
            <p><i class="fas fa-dollar-sign"></i> Price: ₹{{ request.price }}</p>
            <p><i class="fas fa-user-tie"></i> Professional: Waiting for assignment</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Update the Accepted Services Section -->
    <section class="dashboard-section">
      <h3>Accepted Services</h3>
      <div class="requests-grid">
        <div v-for="request in acceptedServices" :key="request.id" class="request-card accepted">
          <div class="request-header">
            <span class="service-name">{{ request.service_name }}</span>
            <span :class="['status-badge', request.is_open ? 'status-open' : 'status-closed']">
              {{ request.is_open ? 'Open' : 'Closed' }}
            </span>
          </div>

          <!-- Professional Details Section -->
          <div class="professional-details">
            <h4><i class="fas fa-user-tie"></i> Professional Details</h4>
            <div class="professional-info">
              <p><strong>Name:</strong> {{ request.professional_name }}</p>
              <p><strong>Experience:</strong> {{ request.experience_years }} years</p>
              <div class="professional-rating" v-if="request.professional_rating">
                <strong>Rating:</strong>
                <div class="stars">
                  <i class="fas fa-star" v-for="n in Math.floor(request.professional_rating)" :key="n"></i>
                  <i class="fas fa-star-half-alt" v-if="request.professional_rating % 1 >= 0.5"></i>
                </div>
                <span class="rating-value">{{ request.professional_rating.toFixed(1) }}/5</span>
              </div>
            </div>
          </div>

          <!-- Service Details Section -->
          <div class="service-details">
            <h4><i class="fas fa-info-circle"></i> Service Details</h4>
            <p><strong>Price:</strong> ₹{{ request.price }}</p>
            <p><strong>Accepted on:</strong> {{ formatDate(request.date_of_request) }}</p>
            <p v-if="request.remarks"><strong>Remarks:</strong> {{ request.remarks }}</p>
          </div>

          <!-- Rate Service Section -->
          <div v-if="request.is_open" class="rate-service-section">
            <button @click="showCloseServiceModal(request)" class="btn-rate-service">
              <i class="fas fa-star"></i> Rate & Close Service
            </button>
            <div class="rating-preview">
              <span>Preview Rating:</span>
              <div class="preview-stars">
                <i v-for="star in 5" 
                   :key="star" 
                   :class="['fas fa-star', { 'active': star <= tempRating }]"
                   @mouseover="tempRating = star"
                   @mouseleave="tempRating = 0"
                ></i>
              </div>
              <span class="preview-hint">Click button above to submit rating</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Update the Service History section -->
    <section class="dashboard-section">
      <h3>Service History</h3>
      <div class="history-grid">
        <div v-for="request in completedServices" :key="request.id" class="history-card">
          <div class="history-header">
            <span class="service-name">{{ request.service_name }}</span>
            <span :class="['status-badge', `status-${request.status}`]">
              {{ request.status }}
            </span>
          </div>
          <div class="history-details">
            <p><i class="fas fa-calendar-check"></i> Completed on: {{ formatDate(request.date_of_completion) }}</p>
            <p><i class="fas fa-dollar-sign"></i> Price: ₹{{ request.price }}</p>
            <p><i class="fas fa-user-tie"></i> Professional: {{ request.professional_name }}</p>
            
            <!-- Rating Section -->
            <div class="rating-section">
              <h4>Rating & Feedback</h4>
              <div v-if="request.rating" class="rating-display">
                <div class="stars">
                  <i v-for="n in request.rating" :key="n" class="fas fa-star"></i>
                </div>
                <span class="rating-value">{{ request.rating }}/5</span>
                <button @click="editRating(request)" class="btn-edit-rating">
                  <i class="fas fa-edit"></i> Edit Rating
                </button>
              </div>
              <div class="remarks-section">
                <p class="remarks-label">Your Remarks:</p>
                <p class="remarks-text">{{ request.remarks || 'No remarks provided' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Add this profile modal section after your existing sections -->
    <div v-if="showProfileModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEditing ? 'Edit Profile' : 'User Profile' }}</h3>
          <button class="close-btn" @click="closeProfile">&times;</button>
        </div>
        <div class="profile-content">
          <div v-if="!isEditing">
            <div class="profile-info">
              <p><strong>Name:</strong> {{ userProfile.name }}</p>
              <p><strong>Email:</strong> {{ userProfile.email }}</p>
              <p><strong>Address:</strong> {{ userProfile.address }}</p>
              <p><strong>Pin Code:</strong> {{ userProfile.pin_code }}</p>
            </div>
            <button @click="startEditing" class="btn-edit">Edit Profile</button>
          </div>
          <div v-else>
            <form @submit.prevent="updateProfile" class="edit-form">
              <div class="form-group">
                <label>Name</label>
                <input type="text" v-model="editedProfile.name" required>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="editedProfile.email" required>
              </div>
              <div class="form-group">
                <label>Address</label>
                <textarea v-model="editedProfile.address" required></textarea>
              </div>
              <div class="form-group">
                <label>Pin Code</label>
                <input type="text" v-model="editedProfile.pin_code" required>
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

    <!-- Add Close Service Modal -->
    <div v-if="showCloseModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Close Service Request</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitCloseService">
            <div class="form-group">
              <label>Rate the Service (1-5)</label>
              <div class="rating-input-container">
                <!-- Numeric Rating Input -->
                <div class="numeric-rating">
                  <button 
                    v-for="n in 5" 
                    :key="n"
                    type="button"
                    :class="['rating-number-btn', { active: closeServiceForm.rating === n }]"
                    @click="closeServiceForm.rating = n"
                  >
                    {{ n }}
                  </button>
                </div>
                <!-- Star Display -->
                <div class="star-rating">
                  <i v-for="n in 5" :key="n" 
                     :class="['fas', n <= closeServiceForm.rating ? 'fa-star' : 'fa-star-o']"
                     class="star-icon"
                  ></i>
                </div>
                <span class="rating-value" v-if="closeServiceForm.rating">
                  Your Rating: {{ closeServiceForm.rating }}/5
                </span>
              </div>
            </div>
            <div class="form-group">
              <label>Remarks</label>
              <textarea 
                v-model="closeServiceForm.remarks" 
                placeholder="Please provide your feedback about the service..."
                required
              ></textarea>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-submit">Submit & Close</button>
              <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Add Edit Rating Modal -->
    <div v-if="showEditRatingModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Edit Rating & Remarks</h3>
          <button class="close-btn" @click="closeEditRatingModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateRating">
            <div class="form-group">
              <label>Update Rating</label>
              <div class="numeric-rating">
                <button 
                  v-for="n in 5" 
                  :key="n"
                  type="button"
                  :class="['rating-number-btn', { active: editRatingForm.rating === n }]"
                  @click="editRatingForm.rating = n"
                >
                  {{ n }}
                </button>
              </div>
              <div class="star-display">
                <i v-for="n in 5" :key="n" 
                   :class="['fas', n <= editRatingForm.rating ? 'fa-star' : 'fa-star-o']"
                   class="star-icon"
                ></i>
              </div>
            </div>
            <div class="form-group">
              <label>Update Remarks</label>
              <textarea 
                v-model="editRatingForm.remarks" 
                placeholder="Add your comments about the service..."
                required
              ></textarea>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-submit">Update Rating</button>
              <button type="button" @click="closeEditRatingModal" class="btn-cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-dashboard {
  min-height: 100vh;
  background: #1a1a1a;
  color: white;
  padding: 20px;
  padding-top: 80px;
}

.dashboard-header {
  background: #242424;
  padding: 15px 30px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-title h2 {
  color: #4CAF50;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
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

.dashboard-section {
  background: #242424;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.dashboard-section h3 {
  color: #4CAF50;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #444;
}

.services-grid, .requests-grid, .history-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 10px;
}

.service-card, .request-card, .history-card {
  background: #2d2d2d;
  border-radius: 10px;
  padding: 20px;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.service-header h4 {
  color: #4CAF50;
  margin: 0;
  font-size: 1.2em;
}

.price {
  color: #4CAF50;
  font-weight: bold;
  font-size: 1.2em;
}

.description {
  color: #ddd;
  margin-bottom: 15px;
  line-height: 1.4;
}

.service-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 15px 0;
  color: #888;
}

.btn-request {
  width: 100%;
  padding: 10px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-request:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.status-badge {
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: 500;
}

.status-requested { background: #ffc107; color: black; }
.status-accepted { background: #17a2b8; color: white; }
.status-completed { background: #28a745; color: white; }
.status-rejected { background: #dc3545; color: white; }

.request-details p {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ddd;
}

.request-details i {
  color: #4CAF50;
  width: 20px;
  text-align: center;
}

.rating-section {
  margin-top: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.rating-input {
  text-align: center;
}

.rating-input h4 {
  color: #4CAF50;
  margin-bottom: 10px;
}

.star-rating {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 15px 0;
}

.star-rating i {
  font-size: 24px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.star-rating i:hover,
.star-rating i.active {
  color: #ffc107;
  transform: scale(1.2);
}

.rating-hint {
  display: block;
  color: #888;
  font-size: 0.9em;
  margin-top: 5px;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.rating-display .stars {
  display: flex;
  gap: 5px;
}

.rating-display .stars i {
  color: #ffc107;
}

.rating-display .rating-value {
  color: #ffc107;
  font-weight: bold;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
    padding: 10px;
  }

  .header-actions {
    width: 100%;
    justify-content: center;
  }

  .header-btn {
    padding: 6px 12px;
    font-size: 0.9em;
  }

  .user-dashboard {
    padding-top: 120px;
  }
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #242424;
  padding: 20px;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #444;
}

.modal-header h3 {
  color: #4CAF50;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}

.modal-body {
  padding: 20px 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  color: #fff;
  margin-bottom: 10px;
  font-weight: 500;
}

.star-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 10px 0;
}

.star-icon {
  color: #ffc107;
  font-size: 28px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.star-icon:hover {
  transform: scale(1.2);
}

.rating-value {
  color: #ffc107;
  font-weight: bold;
  margin-left: 10px;
  font-size: 1.2em;
}

textarea {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  border: 1px solid #444;
  border-radius: 8px;
  background: #333;
  color: #fff;
  resize: vertical;
  font-size: 1em;
}

textarea:focus {
  outline: none;
  border-color: #4CAF50;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.btn-submit {
  flex: 1;
  padding: 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-cancel {
  flex: 1;
  padding: 12px;
  background: #666;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background: #777;
  transform: translateY(-2px);
}

.fa-star {
  color: #ffc107;
}

.fa-star-o {
  color: #666;
}

.professional-details, .service-details {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  margin: 15px 0;
}

.professional-details h4, .service-details h4 {
  color: #4CAF50;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.professional-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.professional-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stars {
  display: flex;
  gap: 3px;
  color: #ffc107;
}

.rating-value {
  color: #ffc107;
  font-weight: bold;
}

.rate-service-section {
  margin-top: 20px;
  padding: 15px;
  background: rgba(76, 175, 80, 0.1);
  border-radius: 8px;
  text-align: center;
}

.btn-rate-service {
  width: 100%;
  padding: 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.btn-rate-service:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.rating-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.preview-stars {
  display: flex;
  gap: 5px;
}

.preview-stars i {
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preview-stars i:hover,
.preview-stars i.active {
  color: #ffc107;
  transform: scale(1.2);
}

.preview-hint {
  color: #888;
  font-size: 0.9em;
  font-style: italic;
}

.status-open {
  background: #17a2b8;
  color: white;
}

.status-closed {
  background: #6c757d;
  color: white;
}

.rating-input-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
}

.numeric-rating {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.rating-number-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #4CAF50;
  background: transparent;
  color: #4CAF50;
  font-size: 1.2em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rating-number-btn:hover {
  background: rgba(76, 175, 80, 0.1);
  transform: translateY(-2px);
}

.rating-number-btn.active {
  background: #4CAF50;
  color: white;
  transform: scale(1.1);
}

.star-rating {
  display: flex;
  gap: 5px;
}

.star-icon {
  font-size: 24px;
  color: #ffc107;
}

.rating-value {
  color: #4CAF50;
  font-weight: bold;
  font-size: 1.2em;
  margin-top: 10px;
}

.fa-star {
  color: #ffc107;
}

.fa-star-o {
  color: #666;
}

.rating-section {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
}

.rating-section h4 {
  color: #4CAF50;
  margin-bottom: 10px;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.stars {
  display: flex;
  gap: 4px;
}

.stars i {
  color: #ffc107;
  font-size: 1.2em;
}

.rating-value {
  color: #ffc107;
  font-weight: bold;
}

.btn-edit-rating {
  background: transparent;
  border: 1px solid #4CAF50;
  color: #4CAF50;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;
}

.btn-edit-rating:hover {
  background: #4CAF50;
  color: white;
}

.remarks-section {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.remarks-label {
  color: #888;
  margin-bottom: 5px;
}

.remarks-text {
  color: #ddd;
  font-style: italic;
  line-height: 1.4;
}

.header-left {
  display: flex;
  flex-direction: column;
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'UserDashboard',
  data() {
    return {
      services: [],
      serviceHistory: [],
      selectedService: null,
      showProfileModal: false,
      userProfile: {
        name: '',
        email: '',
        address: '',
        pin_code: ''
      },
      isEditing: false,
      editedProfile: {
        name: '',
        email: '',
        address: '',
        pin_code: ''
      },
      tempRating: 0,
      showCloseModal: false,
      selectedRequest: null,
      closeServiceForm: {
        rating: 0,
        remarks: ''
      },
      showEditRatingModal: false,
      editRatingForm: {
        rating: 0,
        remarks: '',
        requestId: null
      }
    };
  },
  created() {
    console.log('Component created');
    this.fetchServices();
    this.fetchServiceHistory();
    this.fetchUserProfile();
  },
  computed: {
    requestedServices() {
      return this.serviceHistory.filter(req => req.status === 'requested');
    },
    completedServices() {
      return this.serviceHistory.filter(req => 
        req.status === 'completed' || req.status === 'rejected' || req.status === 'accepted'
      );
    },
    acceptedServices() {
      return this.serviceHistory.filter(req => req.status === 'accepted').map(req => ({
        ...req,
        is_open: !req.date_of_completion  // Service is open if it has no completion date
      }));
    }
  },
  methods: {
    async fetchServices() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/listservices', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        // Get professionals for each service
        const servicesWithProfessionals = await Promise.all(
          response.data.services.map(async (service) => {
            try {
              const profResponse = await axios.get(`http://127.0.0.1:5000/service/${service.id}/providers`, {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              });
              return {
                ...service,
                professionals: profResponse.data.providers
              };
            } catch (error) {
              console.error(`Error fetching professionals for service ${service.id}:`, error);
              return {
                ...service,
                professionals: []
              };
            }
          })
        );

        this.services = servicesWithProfessionals;
        console.log('Services with professionals:', this.services);
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },

    async fetchServiceHistory() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/customer/service_history', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.serviceHistory = response.data.history;
        
        // Initialize temporary ratings
        this.serviceHistory.forEach(request => {
          if (!request.rating) {
            this.$set(this.tempRating, request.id, 0);
          }
        });
        
        console.log('Service history with ratings:', this.serviceHistory);
      } catch (error) {
        console.error('Error fetching service history:', error);
      }
    },

    async requestService(service) {
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://127.0.0.1:5000/customer/service_request', {
          service_id: service.id
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        alert('Service requested successfully!');
        await this.fetchServiceHistory(); // Refresh the history after request
      } catch (error) {
        console.error('Error requesting service:', error);
        alert('Error requesting service');
      }
    },

    async submitRating(requestId, rating) {
      try {
        const token = localStorage.getItem('token');
        await axios.post(`http://127.0.0.1:5000/customer/service_request/${requestId}/complete`, {
          rating: rating,
          remarks: 'Service completed successfully'
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        alert('Rating submitted successfully!');
        await this.fetchServiceHistory(); // Refresh the history
      } catch (error) {
        console.error('Error submitting rating:', error);
        alert('Error submitting rating');
      }
    },

    async showProfile() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/customer/profile', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.userProfile = response.data;
        this.showProfileModal = true;
        console.log('Profile data:', this.userProfile); // Debug log
      } catch (error) {
        console.error('Error fetching profile:', error);
        alert('Error fetching profile');
      }
    },

    async handleLogout() {
      try {
        localStorage.removeItem('token');
        localStorage.removeItem('userRole');
        await axios.get('http://127.0.0.1:5000/logout');
        this.$router.push('/login');
      } catch (error) {
        console.error('Logout error:', error);
        localStorage.clear();
        this.$router.push('/login');
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString();
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
    },

    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        await axios.put('http://127.0.0.1:5000/customer/profile', this.editedProfile, {
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

    async fetchUserProfile() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/customer/profile', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.userProfile = response.data;
        console.log('User profile:', this.userProfile); // Debug log
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    },

    showCloseServiceModal(request) {
      this.selectedRequest = request;
      this.closeServiceForm = {
        rating: 0,
        remarks: ''
      };
      this.showCloseModal = true;
    },

    closeModal() {
      this.showCloseModal = false;
      this.selectedRequest = null;
      this.closeServiceForm = {
        rating: 0,
        remarks: ''
      };
    },

    async submitCloseService() {
      if (!this.closeServiceForm.rating) {
        alert('Please provide a rating');
        return;
      }

      try {
        const token = localStorage.getItem('token');
        await axios.post(`http://127.0.0.1:5000/customer/service_request/${this.selectedRequest.id}/complete`, {
          rating: this.closeServiceForm.rating,
          remarks: this.closeServiceForm.remarks
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        alert('Service closed successfully!');
        this.closeModal();
        await this.fetchServiceHistory();
      } catch (error) {
        console.error('Error closing service:', error);
        alert('Error closing service');
      }
    },

    editRating(request) {
      this.editRatingForm = {
        rating: request.rating,
        remarks: request.remarks,
        requestId: request.id
      };
      this.showEditRatingModal = true;
    },

    closeEditRatingModal() {
      this.showEditRatingModal = false;
      this.editRatingForm = {
        rating: 0,
        remarks: '',
        requestId: null
      };
    },

    async updateRating() {
      try {
        const token = localStorage.getItem('token');
        await axios.post(`http://127.0.0.1:5000/customer/service_request/${this.editRatingForm.requestId}/complete`, {
          rating: this.editRatingForm.rating,
          remarks: this.editRatingForm.remarks
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        alert('Rating updated successfully!');
        this.closeEditRatingModal();
        await this.fetchServiceHistory();
      } catch (error) {
        console.error('Error updating rating:', error);
        alert('Error updating rating');
      }
    }
  }
};
</script>
