<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
#app {
  margin-top: 60px;
}


</style>

<script>
export default {
  created() {
    // Check authentication status when app starts
    this.checkAuth();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('token');
      const userRole = localStorage.getItem('userRole');
      const currentPath = this.$route.path;

      // If on a protected route without authentication
      if (!token && currentPath !== '/login' && 
          currentPath !== '/signup' && 
          currentPath !== '/signup/service-provider') {
        this.$router.push('/login');
        return;
      }

      // If authenticated but on wrong dashboard
      if (token && userRole) {
        const correctPath = this.getCorrectPath(userRole);
        if (this.isOnWrongDashboard(currentPath, userRole)) {
          this.$router.push(correctPath);
        }
      }
    },

    getCorrectPath(role) {
      switch (role) {
        case 'admin':
          return '/admin';
        case 'customer':
          return '/user';
        case 'service_professional':
          return '/serviceprovider';
        default:
          return '/login';
      }
    },

    isOnWrongDashboard(currentPath, role) {
      const adminPaths = ['/admin', '/admin/service', '/admin/users', '/admin/search'];
      const customerPaths = ['/user'];
      const professionalPaths = ['/serviceprovider'];

      if (role === 'admin' && !adminPaths.some(path => currentPath.startsWith(path))) {
        return true;
      }
      if (role === 'customer' && !customerPaths.some(path => currentPath.startsWith(path))) {
        return true;
      }
      if (role === 'service_professional' && !professionalPaths.some(path => currentPath.startsWith(path))) {
        return true;
      }
      return false;
    }
  }
};
</script>
