<template>
  <div class="list-professionals">
    <h2>All Service Professionals</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-if="professionals.length === 0">No service professionals found.</div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Name</th>
            <th>Email</th>
            <th>Address</th>
            <th>Pin Code</th>
            <th>Service Name</th>
            <th>Experience Years</th>
            <th>Document Upload</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.id">
            <td>{{ professional.id }}</td>
            <td>{{ professional.username }}</td>
            <td>{{ professional.name }}</td>
            <td>{{ professional.email }}</td>
            <td>{{ professional.address }}</td>
            <td>{{ professional.pin_code }}</td>
            <td>{{ professional.service_name }}</td>
            <td>{{ professional.experience_years }}</td>
            <td>
              <a :href="professional.document_upload" target="_blank">
                View Document
              </a>
            </td>
            <td>{{ professional.is_blocked ? "Blocked" : "Active" }}</td>
            <td>
              <button 
                @click="toggleBlockStatus(professional)" 
                :class="{ 'btn-unblock': professional.is_blocked, 'btn-block': !professional.is_blocked }">
                {{ professional.is_blocked ? 'Unblock' : 'Block' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      professionals: [],
      loading: false,
      apiUrl: "http://127.0.0.1:5000/service-professionals", // Backend URL
    };
  },
  created() {
    this.fetchProfessionals();
  },
  methods: {
    async fetchProfessionals() {
      this.loading = true;
      try {
        const response = await this.$axios.get(`${this.apiUrl}/service-professionals`);
        console.log('Fetched professionals:', response.data); // Log the entire response for debugging
        this.professionals = response.data['service-professionals'] || []; // Handle empty response
      } catch (error) {
        console.error('Error fetching professionals:', error);
      } finally {
        this.loading = false;
      }
    },
    async toggleBlockStatus(professional) {
      try {
        console.log(professional.id); // Just an example of using the professional object
  } catch (error) {
    console.error('Error toggling block status:', error);}
    },
  },
};
</script>
