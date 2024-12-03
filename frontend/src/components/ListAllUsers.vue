<template>
  <div class="list-users">
    <h2>All Users</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Name</th>
          <th>Email</th>
          <th>Address</th>
          <th>Pin Code</th>
          <th>Status</th>
          <th>Role</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.address }}</td>
          <td>{{ user.pin_code }}</td>
          <td>{{ user.is_blocked ? "Blocked" : "Active" }}</td>
          <td>{{ user.role }}</td>
          <td>
            <button 
              @click="toggleBlockStatus(user)" 
              :class="user.is_blocked ? 'btn-unblock' : 'btn-block'">
              {{ user.is_blocked ? 'Unblock' : 'Block' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await this.$axios.get('/admin/users');
        this.users = response.data.users;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async toggleBlockStatus(user) {
      try {
        const action = user.is_blocked ? 'unblock' : 'block';
        await this.$axios.put(`/admin/user/${user.id}/${action}`);
        user.is_blocked = !user.is_blocked; // Toggle the status
      } catch (error) {
        console.error('Error toggling block status:', error);
      }
    },
  },
};
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  padding: 10px;
  border: 1px solid #ddd;
}

button {
  padding: 5px 10px;
  cursor: pointer;
  border: none;
}

.btn-block {
  background-color: red;
  color: white;
}

.btn-unblock {
  background-color: green;
  color: white;
}
</style>
