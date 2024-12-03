<template>
  <div class="search-service-request">
    <h2>Search Service Requests</h2>
    <div class="search-container">
      <label for="searchBy">Search by:</label>
      <select v-model="searchBy" id="searchBy" class="form-control">
        <option value="status">Status</option>
        <option value="customer">Customer Name</option>
        <option value="professional">Professional Name</option>
        <option value="date">Date</option>
      </select>

      <div class="search-input-container">
        <input 
          v-if="searchBy !== 'date'"
          type="text" 
          v-model="searchText" 
          :placeholder="`Search by ${searchBy}...`"
          class="form-control"
        />
        <input 
          v-else
          type="date" 
          v-model="searchText" 
          class="form-control"
        />
      </div>

      <button @click="performSearch" class="btn-search">Search</button>
    </div>

    <!-- Display Search Results -->
    <div v-if="loading" class="loading">
      Searching...
    </div>
    <div v-else>
      <div v-if="searchResults.length" class="results-container">
        <h3>Search Results:</h3>
        <table class="results-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Professional</th>
              <th>Service</th>
              <th>Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in searchResults" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.professional_name || 'Not Assigned' }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ formatDate(request.date_of_request) }}</td>
              <td>
                <span :class="getStatusClass(request.status)">
                  {{ request.status }}
                </span>
              </td>
              <td>
                <button 
                  @click="viewDetails(request)" 
                  class="btn-view"
                >
                  View Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="hasSearched" class="no-results">
        No results found for your search criteria
      </div>
    </div>

    <!-- Request Details Modal -->
    <div v-if="selectedRequest" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Request Details</h3>
          <button class="close-btn" @click="closeDetails">&times;</button>
        </div>
        <div class="request-details">
          <div class="detail-section">
            <h4>Service Information</h4>
            <p><strong>Service:</strong> {{ selectedRequest.service_name }}</p>
            <p><strong>Status:</strong> 
              <span :class="getStatusClass(selectedRequest.status)">
                {{ selectedRequest.status }}
              </span>
            </p>
            <p><strong>Date Requested:</strong> {{ formatDate(selectedRequest.date_of_request) }}</p>
          </div>

          <div class="detail-section">
            <h4>Customer Information</h4>
            <p><strong>Name:</strong> {{ selectedRequest.customer_name }}</p>
            <p><strong>Email:</strong> {{ selectedRequest.customer_email }}</p>
            <p><strong>Address:</strong> {{ selectedRequest.address }}</p>
          </div>

          <div class="detail-section" v-if="selectedRequest.professional_name">
            <h4>Professional Information</h4>
            <p><strong>Name:</strong> {{ selectedRequest.professional_name }}</p>
            <p><strong>Email:</strong> {{ selectedRequest.professional_email }}</p>
          </div>

          <div class="detail-section">
            <h4>Additional Information</h4>
            <p><strong>Remarks:</strong> {{ selectedRequest.remarks || 'No remarks' }}</p>
          </div>

          <div class="modal-actions">
            <button class="btn-close" @click="closeDetails">Close</button>
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
      searchBy: 'status',
      searchText: '',
      searchResults: [],
      loading: false,
      hasSearched: false,
      selectedRequest: null,
    };
  },
  methods: {
    async performSearch() {
      this.loading = true;
      this.hasSearched = true;
      
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://127.0.0.1:5000/admin/search-requests`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          params: {
            searchBy: this.searchBy,
            searchText: this.searchText
          }
        });
        
        this.searchResults = response.data.requests;
      } catch (error) {
        console.error('Search error:', error);
        alert('Error performing search');
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },

    getStatusClass(status) {
      const statusClasses = {
        'requested': 'status-requested',
        'assigned': 'status-assigned',
        'in_progress': 'status-progress',
        'completed': 'status-completed',
        'cancelled': 'status-cancelled'
      };
      return statusClasses[status] || 'status-default';
    },

    viewDetails(request) {
      this.selectedRequest = request;
    },

    closeDetails() {
      this.selectedRequest = null;
    }
  }
};
</script>

<style scoped>
.search-service-request {
  padding: 20px;
}

.search-container {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 30px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-input-container {
  flex-grow: 1;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
}

select.form-control {
  min-width: 150px;
}

.btn-search {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-search:hover {
  background-color: #0056b3;
}

.results-container {
  margin-top: 20px;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.results-table th,
.results-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.results-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.status-requested { color: #ffc107; }
.status-assigned { color: #17a2b8; }
.status-progress { color: #007bff; }
.status-completed { color: #28a745; }
.status-cancelled { color: #dc3545; }
.status-default { color: #6c757d; }

.btn-view {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-view:hover {
  background-color: #5a6268;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #6c757d;
  background: #f8f9fa;
  border-radius: 4px;
  margin-top: 20px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #007bff;
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 600px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #dee2e6;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
}

.request-details {
  padding: 20px;
}

.detail-section {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.detail-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>
  