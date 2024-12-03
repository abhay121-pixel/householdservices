<template>
    <div>
      <h1>Admin - List of Services</h1>
      <ul>
        <li v-for="service in services" :key="service.id">
          {{ service.name }} - {{ service.price }} - {{ service.time_required }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        services: [],
      };
    },
    created() {
      this.fetchServices();
    },
    methods: {
      fetchServices() {
        axios
          .get('/admin/listservices') // Use the same endpoint for listing services
          .then((response) => {
            this.services = response.data.services;
          })
          .catch((error) => {
            console.error("Error fetching services:", error);
          });
      },
    },
  };
  </script>
  