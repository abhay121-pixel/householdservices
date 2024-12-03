<template>
  <div class="summary-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h2>Service History</h2>
          <span class="subtitle">Overview of all service requests</span>
        </div>
        <button @click="goBack" class="header-btn">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </button>
      </div>
    </header>

    <!-- Service History Table Section -->
    <section class="history-section">
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Service</th>
              <th>Customer</th>
              <th>Professional</th>
              <th>Status</th>
              <th>Request Date</th>
              <th>Completion Date</th>
              <th>Rating</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceHistory" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.professional_name || 'Not Assigned' }}</td>
              <td>
                <span :class="['status-badge', `status-${request.status.toLowerCase()}`]">
                  {{ request.status }}
                </span>
              </td>
              <td>{{ formatDate(request.date_of_request) }}</td>
              <td>{{ request.date_of_completion ? formatDate(request.date_of_completion) : 'N/A' }}</td>
              <td>
                <div v-if="request.rating" class="rating-display">
                  <i class="fas fa-star"></i>
                  <span>{{ request.rating }}/5</span>
                </div>
                <span v-else>No Rating</span>
              </td>
              <td>{{ request.remarks || 'No remarks' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SummaryCharts',
  data() {
    return {
      serviceHistory: []
    };
  },
  methods: {
    goBack() {
      this.$router.push('/admin');
    },
    async fetchData() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/service-requests', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.serviceHistory = response.data.requests;
        console.log('Service history:', this.serviceHistory);
      } catch (error) {
        console.error('Error fetching service history:', error);
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString();
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.summary-dashboard {
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #fff;
  padding: 20px;
  padding-top: 100px;
}

.dashboard-header {
  background: #242424;
  padding: 15px 30px;
  margin-bottom: 30px;
  border-radius: 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  flex-direction: column;
}

.header-left h2 {
  color: #4CAF50;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.subtitle {
  color: #888;
  font-size: 14px;
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
  transform: translateY(-2px);
}

.history-section {
  background: #242424;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
}

.table-container {
  overflow-x: auto;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  color: #fff;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  background: rgba(0, 0, 0, 0.2);
  color: #4CAF50;
  font-weight: 600;
}

tr:hover {
  background: rgba(255, 255, 255, 0.05);
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

.rating-display {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #ffc107;
}

.rating-display i {
  font-size: 1em;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .header-btn {
    width: 100%;
    justify-content: center;
  }

  .summary-dashboard {
    padding-top: 140px;
  }
}
</style>
  