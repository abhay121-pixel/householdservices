<template>
  <div class="admin-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h2>Admin Dashboard</h2>
        </div>
        <div class="header-actions">
          <button @click="goToSummary" class="header-btn">
            <i class="fas fa-chart-line"></i> Summary
          </button>
          <button @click="downloadAllData" class="header-btn">
            <i class="fas fa-download"></i> Download Data
          </button>
          <button @click="handleLogout" class="header-btn">
            <i class="fas fa-sign-out-alt"></i> Logout
          </button>
        </div>
      </div>
    </header>

    <!-- Add this after the header section -->
    <div class="search-section">
      <div class="search-container">
        <select v-model="searchSection" class="search-select">
          <option value="users">Search Users</option>
          <option value="professionals">Search Professionals</option>
          <option value="services">Search Services</option>
        </select>
        <div class="search-input-wrapper">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            v-model="searchQuery" 
            :placeholder="getSearchPlaceholder()"
            class="search-input"
            @input="handleSearch"
          />
        </div>
      </div>
    </div>

    <!-- Users Section -->
    <section class="dashboard-section">
      <h3>Users</h3>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role }}</td>
              <td>{{ user.is_blocked ? 'Blocked' : 'Active' }}</td>
              <td>
                <button @click="toggleUserBlockStatus(user)" class="btn-action">
                  {{ user.is_blocked ? 'Unblock' : 'Block' }}
                </button>
                <button @click="viewUserProfile(user)" class="btn-view">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Service Professionals Section -->
    <section class="dashboard-section">
      <h3>Service Professionals</h3>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Service</th>
              <th>Experience</th>
              <th>Block Status</th>
              <th>Approval Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in filteredProfessionals" :key="professional.id">
              <td>{{ professional.id }}</td>
              <td>{{ professional.name }}</td>
              <td>{{ professional.service_name }}</td>
              <td>{{ professional.experience_years }} years</td>
              <td>
                <span :class="['status-badge', professional.is_blocked ? 'status-blocked' : 'status-active']">
                  {{ professional.is_blocked ? 'Blocked' : 'Active' }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', professional.is_approved ? 'status-approved' : 'status-pending']">
                  {{ professional.is_approved ? 'Approved' : 'Pending' }}
                </span>
              </td>
              <td>
                <button @click="toggleProfessionalBlockStatus(professional)" class="btn-action">
                  {{ professional.is_blocked ? 'Unblock' : 'Block' }}
                </button>
                <button @click="toggleProfessionalApproval(professional)" class="btn-approve">
                  {{ professional.is_approved ? 'Unapprove' : 'Approve' }}
                </button>
                <button @click="viewProfessionalProfile(professional)" class="btn-view">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Services Section -->
    <section class="dashboard-section">
      <h3>Services</h3>
      <button @click="showAddServiceModal" class="btn-add">Add New Service</button>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Time Required</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in filteredServices" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.name }}</td>
              <td>{{ service.description }}</td>
              <td>₹{{ service.price }}</td>
              <td>{{ service.time_required }}</td>
              <td>
                <button @click="editService(service)" class="btn-edit">Edit</button>
                <button @click="deleteService(service.id)" class="btn-delete">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- User Profile Modal -->
    <div v-if="selectedUser" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>User Profile</h3>
          <button class="close-btn" @click="closeUserProfile">&times;</button>
        </div>
        <div class="profile-content">
          <div class="profile-section">
            <h4>Basic Information</h4>
            <p><strong>Name:</strong> {{ selectedUser.name }}</p>
            <p><strong>Username:</strong> {{ selectedUser.username }}</p>
            <p><strong>Email:</strong> {{ selectedUser.email }}</p>
            <p><strong>Role:</strong> {{ selectedUser.role }}</p>
          </div>

          <div class="profile-section">
            <h4>Contact Details</h4>
            <p><strong>Address:</strong> {{ selectedUser.address }}</p>
            <p><strong>Pin Code:</strong> {{ selectedUser.pin_code }}</p>
          </div>

          <div class="profile-section">
            <h4>Account Status</h4>
            <p><strong>Status:</strong> 
              <span :class="selectedUser.is_blocked ? 'status-blocked' : 'status-active'">
                {{ selectedUser.is_blocked ? 'Blocked' : 'Active' }}
              </span>
            </p>
            <p><strong>Created On:</strong> {{ formatDate(selectedUser.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Professional Profile Modal -->
    <div v-if="selectedProfessional" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Professional Profile</h3>
          <button class="close-btn" @click="closeProfessionalProfile">&times;</button>
        </div>
        <div class="profile-content">
          <div class="profile-section">
            <h4>Basic Information</h4>
            <p><strong>Name:</strong> {{ selectedProfessional.name }}</p>
            <p><strong>Username:</strong> {{ selectedProfessional.username }}</p>
            <p><strong>Email:</strong> {{ selectedProfessional.email }}</p>
          </div>

          <div class="profile-section">
            <h4>Professional Details</h4>
            <p><strong>Service:</strong> {{ selectedProfessional.service_name }}</p>
            <p><strong>Experience:</strong> {{ selectedProfessional.experience_years }} years</p>
            <p><strong>Average Rating:</strong> 
              <span class="rating-display">
                <i class="fas fa-star"></i> 
                {{ selectedProfessional.average_rating?.toFixed(1) || 'No ratings' }}
              </span>
            </p>
          </div>

          <div class="profile-section">
            <h4>Contact Details</h4>
            <p><strong>Address:</strong> {{ selectedProfessional.address }}</p>
            <p><strong>Pin Code:</strong> {{ selectedProfessional.pin_code }}</p>
          </div>

          <div class="profile-section">
            <h4>Account Status</h4>
            <p><strong>Status:</strong> 
              <span :class="['status-badge', selectedProfessional.is_blocked ? 'status-blocked' : 'status-active']">
                {{ selectedProfessional.is_blocked ? 'Blocked' : 'Active' }}
              </span>
            </p>
            <p><strong>Approval:</strong>
              <span :class="['status-badge', selectedProfessional.is_approved ? 'status-approved' : 'status-pending']">
                {{ selectedProfessional.is_approved ? 'Approved' : 'Pending' }}
              </span>
            </p>
            <p><strong>Created On:</strong> {{ formatDate(selectedProfessional.created_at) }}</p>
          </div>

          <div class="profile-section" v-if="selectedProfessional.document_upload">
            <h4>Documents</h4>
            <a :href="selectedProfessional.document_upload" target="_blank" class="document-link">
              <i class="fas fa-file-alt"></i> View Uploaded Document
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Service Edit Modal -->
    <div v-if="showServiceModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editingService ? 'Edit Service' : 'Add New Service' }}</h3>
          <button class="close-btn" @click="closeServiceModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitService">
            <div class="form-group">
              <label>Service Name</label>
              <input type="text" v-model="serviceForm.name" required>
            </div>
            <div class="form-group">
              <label>Description</label>
              <textarea v-model="serviceForm.description" required></textarea>
            </div>
            <div class="form-group">
              <label>Price (₹)</label>
              <input type="number" v-model="serviceForm.price" required>
            </div>
            <div class="form-group">
              <label>Time Required</label>
              <input type="text" v-model="serviceForm.time_required" required>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-save">
                {{ editingService ? 'Save Changes' : 'Add Service' }}
              </button>
              <button type="button" @click="closeServiceModal" class="btn-cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  padding: 20px;
  min-height: 100vh;
  color: white;
  position: relative;
  overflow: hidden;
  padding-top: 80px;
  background-image: url('https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.admin-dashboard::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(26, 26, 26, 0.95),
    rgba(26, 26, 26, 0.85)
  );
  z-index: 0;
}

.dashboard-header,
.search-section,
.dashboard-section {
  position: relative;
  z-index: 1;
  backdrop-filter: blur(5px);
  background: rgba(36, 36, 36, 0.95);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.dashboard-section {
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashboard-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.search-section {
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin: 20px 0;
  padding: 20px;
  border-radius: 10px;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header-left {
  text-align: left;
}

.header-left h2 {
  font-size: 28px;
  margin: 0;
  color: white;
}

.subtitle {
  color: rgba(255,255,255,0.8);
  font-size: 16px;
}

.stats-container {
  display: flex;
  gap: 20px;
  margin: 10px 0;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 15px 20px;
  border-radius: 12px;
  flex: 1;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.15);
}

.stat-icon {
  background: rgba(255, 255, 255, 0.15);
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon i {
  font-size: 24px;
  color: white;
}

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: white;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.btn-summary, .btn-download, .btn-logout {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-summary {
  background: rgba(255, 255, 255, 0.2);
}

.btn-download {
  background: rgba(255, 255, 255, 0.2);
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
}

.btn-summary:hover, .btn-download:hover, .btn-logout:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.3);
}

@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
  }

  .header-actions {
    flex-direction: column;
  }

  .btn-summary, .btn-download, .btn-logout {
    width: 100%;
    justify-content: center;
  }
}

.dashboard-section {
  background: #242424;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #444;
}

th {
  background-color: #333;
  color: white;
}

.btn-action, .btn-approve, .btn-view, .btn-edit, .btn-delete, .btn-add {
  padding: 6px 12px;
  margin: 0 4px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-action { background: #4CAF50; color: white; }
.btn-approve { background: #2196F3; color: white; }
.btn-view { background: #9C27B0; color: white; }
.btn-edit { background: #FF9800; color: white; }
.btn-delete { background: #f44336; color: white; }
.btn-add { background: #4CAF50; color: white; margin-bottom: 10px; }

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #242424;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
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
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}

.profile-section {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #444;
}

.profile-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.profile-section h4 {
  color: #4CAF50;
  margin-bottom: 15px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: 500;
  display: inline-block;
}

.status-active {
  background-color: #28a745;
  color: white;
}

.status-blocked {
  background-color: #dc3545;
  color: white;
}

.status-approved {
  background-color: #28a745;
  color: white;
}

.status-pending {
  background-color: #ffc107;
  color: black;
}

.document-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #4CAF50;
  text-decoration: none;
  padding: 8px 12px;
  background: rgba(76, 175, 80, 0.1);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.document-link:hover {
  background: rgba(76, 175, 80, 0.2);
  transform: translateY(-2px);
}

.rating-display {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #ffc107;
}

.rating-display i {
  font-size: 1.1em;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #fff;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #444;
  border-radius: 4px;
  background: #333;
  color: #fff;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-save {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  background: #666;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.search-section {
  margin: 20px 0;
  padding: 20px;
  background: #242424;
  border-radius: 10px;
}

.search-container {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-select {
  padding: 10px 15px;
  border-radius: 8px;
  background: #333;
  color: white;
  border: 1px solid #444;
  min-width: 150px;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
}

.search-input-wrapper i {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-input {
  width: 100%;
  padding: 10px 15px 10px 40px;
  border-radius: 8px;
  background: #333;
  color: white;
  border: 1px solid #444;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
}

@media (max-width: 768px) {
  .search-container {
    flex-direction: column;
  }
  
  .search-select {
    width: 100%;
  }
}

@keyframes floralFloat {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 40px 40px;
  }
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

  .admin-dashboard {
    padding-top: 120px;
  }
}

.header-left {
  display: flex;
  flex-direction: column;
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      users: [],
      professionals: [],
      services: [],
      showServiceModal: false,
      editingService: false,
      serviceForm: {
        name: '',
        description: '',
        price: '',
        time_required: ''
      },
      searchQuery: '',
      searchSection: 'users',
      filteredUsers: [],
      filteredProfessionals: [],
      filteredServices: [],
      searchType: 'name',
      selectedUser: null,
      selectedProfessional: null,
    };
  },
  created() {
    this.fetchUsers();
    this.fetchProfessionals();
    this.fetchServices();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/users', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.users = response.data.users;
        this.filteredUsers = [...this.users];
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },

    async fetchProfessionals() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/service-professionals', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.professionals = response.data['service-professionals'];
        this.filteredProfessionals = [...this.professionals];
      } catch (error) {
        console.error('Error fetching professionals:', error);
      }
    },

    async fetchServices() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/listservices', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.services = response.data.services;
        this.filteredServices = [...this.services];
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },

    async toggleUserBlockStatus(user) {
      try {
        const token = localStorage.getItem('token');
        const action = user.is_blocked ? 'unblock' : 'block';
        await axios.post(`http://127.0.0.1:5000/admin/user/${user.id}/${action}`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        await this.fetchUsers();
      } catch (error) {
        console.error('Error toggling user block status:', error);
      }
    },

    async toggleProfessionalBlockStatus(professional) {
      try {
        const token = localStorage.getItem('token');
        const action = professional.is_blocked ? 'unblock' : 'block';
        await axios.post(`http://127.0.0.1:5000/admin/professional/${professional.id}/${action}/block`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        await this.fetchProfessionals();
      } catch (error) {
        console.error('Error toggling professional block status:', error);
        alert('Error updating professional status');
      }
    },

    async toggleProfessionalApproval(professional) {
      try {
        const token = localStorage.getItem('token');
        const action = professional.is_approved ? 'unapprove' : 'approve';
        await axios.post(`http://127.0.0.1:5000/admin/professional/${professional.id}/${action}/approval`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        await this.fetchProfessionals();
      } catch (error) {
        console.error('Error toggling professional approval:', error);
        alert('Error updating professional status');
      }
    },

    showAddServiceModal() {
      this.editingService = false;
      this.serviceForm = {
        name: '',
        description: '',
        price: '',
        time_required: ''
      };
      this.showServiceModal = true;
    },

    editService(service) {
      this.editingService = true;
      this.serviceForm = { ...service };
      this.showServiceModal = true;
    },

    async submitService() {
      try {
        const token = localStorage.getItem('token');
        if (this.editingService) {
          await axios.put(`http://127.0.0.1:5000/admin/service/${this.serviceForm.id}`, this.serviceForm, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
        } else {
          await axios.post('http://127.0.0.1:5000/admin/service', this.serviceForm, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
        }
        this.closeServiceModal();
        await this.fetchServices();
        alert(this.editingService ? 'Service updated successfully!' : 'Service added successfully!');
      } catch (error) {
        console.error('Error submitting service:', error);
        alert('Error saving service');
      }
    },

    closeServiceModal() {
      this.showServiceModal = false;
      this.editingService = false;
      this.serviceForm = {
        name: '',
        description: '',
        price: '',
        time_required: ''
      };
    },

    async deleteService(serviceId) {
      if (confirm('Are you sure you want to delete this service?')) {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.delete(`http://127.0.0.1:5000/admin/service/${serviceId}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          if (response.status === 200) {
            // Remove the service from both arrays
            this.services = this.services.filter(service => service.id !== serviceId);
            this.filteredServices = this.filteredServices.filter(service => service.id !== serviceId);
            alert('Service deleted successfully!');
            // Refresh the services list
            await this.fetchServices();
          }
        } catch (error) {
          console.error('Error deleting service:', error);
          alert(error.response?.data?.message || 'Failed to delete service. Please try again.');
        }
      }
    },

    async viewUserProfile(user) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://127.0.0.1:5000/admin/user/${user.id}/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.selectedUser = response.data;
      } catch (error) {
        console.error('Error fetching user profile:', error);
        alert('Error fetching user profile');
      }
    },

    closeUserProfile() {
      this.selectedUser = null;
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString();
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

    downloadCSV(headers, data, filename) {
      // Create CSV content
      const csvContent = [
        headers.join(','),
        ...data.map(row => row.join(','))
      ].join('\n');

      // Create blob and download link
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      
      if (navigator.msSaveBlob) { // For IE
        navigator.msSaveBlob(blob, filename);
      } else {
        link.href = URL.createObjectURL(blob);
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    },

    downloadAllData() {
      try {
        // Download Users Data
        const usersHeaders = ['ID', 'Name', 'Email', 'Role', 'Status'];
        const usersData = this.users.map(user => [
          user.id,
          user.name,
          user.email,
          user.role,
          user.is_blocked ? 'Blocked' : 'Active'
        ]);
        this.downloadCSV(usersHeaders, usersData, 'users_list.csv');

        // Download Professionals Data
        const professionalsHeaders = ['ID', 'Name', 'Service', 'Experience', 'Status', 'Approval'];
        const professionalsData = this.professionals.map(prof => [
          prof.id,
          prof.name,
          prof.service_name,
          prof.experience_years + ' years',
          prof.is_blocked ? 'Blocked' : 'Active',
          prof.is_approved ? 'Approved' : 'Pending'
        ]);
        this.downloadCSV(professionalsHeaders, professionalsData, 'professionals_list.csv');

        // Download Services Data
        const servicesHeaders = ['ID', 'Name', 'Description', 'Price', 'Time Required'];
        const servicesData = this.services.map(service => [
          service.id,
          service.name,
          service.description,
          service.price,
          service.time_required
        ]);
        this.downloadCSV(servicesHeaders, servicesData, 'services_list.csv');

        alert('All data has been downloaded successfully!');
      } catch (error) {
        console.error('Error downloading data:', error);
        alert('Error downloading data. Please try again.');
      }
    },

    getSearchPlaceholder() {
      switch(this.searchSection) {
        case 'users':
          return 'Search users by name or email...';
        case 'professionals':
          return 'Search professionals by name, service, or email...';
        case 'services':
          return 'Search services by name...';
        default:
          return 'Search...';
      }
    },

    handleSearch() {
      const query = this.searchQuery.toLowerCase().trim();
      
      switch(this.searchSection) {
        case 'users':
          this.filteredUsers = this.users.filter(user => 
            user.name?.toLowerCase().includes(query) ||
            user.email?.toLowerCase().includes(query) ||
            user.role?.toLowerCase().includes(query)
          );
          break;
        
        case 'professionals':
          this.filteredProfessionals = this.professionals.filter(prof => 
            prof.name?.toLowerCase().includes(query) ||
            prof.email?.toLowerCase().includes(query) ||
            prof.service_name?.toLowerCase().includes(query)
          );
          break;
        
        case 'services':
          this.filteredServices = this.services.filter(service => 
            service.name?.toLowerCase().includes(query) ||
            service.description?.toLowerCase().includes(query)
          );
          break;
      }
    },

    async viewProfessionalProfile(professional) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://127.0.0.1:5000/admin/professional/${professional.id}/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.selectedProfessional = response.data;
      } catch (error) {
        console.error('Error fetching professional profile:', error);
        alert('Error fetching professional profile');
      }
    },

    closeProfessionalProfile() {
      this.selectedProfessional = null;
    },

    getStatusClass(status) {
      return `status-${status.toLowerCase()}`;
    },

    goToSummary() {
      this.$router.push('/admin/summary');
    },

    showHistory() {
      // Set the search section to requests
      this.searchSection = 'requests';
      this.searchQuery = '';  // Clear any existing search
      
      // Filter to show only completed and rejected requests
      this.filteredServiceRequests = this.serviceRequests.filter(request => 
        request.status === 'completed' || request.status === 'rejected'
      );

      // Add a small delay to ensure the DOM is updated
      setTimeout(() => {
        // Find the service requests section
        const requestsSection = document.querySelector('.dashboard-section:last-child');
        if (requestsSection) {
          // Scroll to the section with smooth animation
          requestsSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
          });
        }
      }, 100);
    },

    showProfile() {
      // Add profile viewing functionality here
      alert('Profile functionality coming soon!');
    }
  },
  watch: {
    searchQuery() {
      this.handleSearch();
    },
    searchSection() {
      this.searchQuery = '';
      this.handleSearch();
    }
  }
};
</script>
