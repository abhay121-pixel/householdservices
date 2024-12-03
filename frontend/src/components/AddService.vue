<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Add Service</h2>
      <form @submit.prevent="addService">
        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>
        <div class="form-group">
          <label for="serviceName">Service Name</label>
          <input
            type="text"
            v-model="serviceName"
            id="serviceName"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            v-model="description"
            id="description"
            class="form-control"
            required
          ></textarea>
        </div>
        <div class="form-group">
          <label for="basePrice">Base Price</label>
          <input
            type="number"
            v-model.number="basePrice"
            id="basePrice"
            class="form-control"
            min="1"
            step="0.01"
            @input="validatePrice"
            required
          />
          <small class="text-danger" v-if="priceError">
            {{ priceError }}
          </small>
        </div>
        <div class="form-group">
          <label for="timeRequired">Time Required</label>
          <input
            type="text"
            v-model="timeRequired"
            id="timeRequired"
            class="form-control"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Add Service</button>
        <button
          type="button"
          class="btn btn-secondary"
          @click="returnToDashboard"
        >
          Return to Dashboard
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'AddService',
  props: {
    categoryId: {
      type: [Number, String],
      required: false,
      default: null
    }
  },
  data() {
    return {
      serviceName: "",
      description: "",
      basePrice: 1,
      timeRequired: "",
      errorMessage: "",
      priceError: "",
      loading: false,
    };
  },
  methods: {
    validatePrice() {
      if (this.basePrice < 1) {
        this.priceError = "Price must be at least 1";
        this.basePrice = 1;
      } else {
        this.priceError = "";
      }
    },
    returnToDashboard() {
      window.location.href = '/admin';  // Force reload when returning to dashboard
    },
    addService() {
      if (!this.serviceName || !this.description || !this.timeRequired) {
        this.errorMessage = "Please fill in all fields";
        return;
      }

      if (this.basePrice < 1) {
        this.errorMessage = "Price must be at least 1";
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        this.errorMessage = "No authentication token found. Please log in.";
        this.$router.push('/login');
        return;
      }

      const serviceData = {
        name: this.serviceName,
        description: this.description,
        price: parseFloat(this.basePrice),
        time_required: this.timeRequired
      };

      console.log('Sending service data:', serviceData);

      axios
        .post("http://127.0.0.1:5000/admin/service", serviceData, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        })
        .then((response) => {
          console.log('Server response:', response.data);
          alert("Service added successfully!");
          window.location.href = '/admin';  // Force reload after adding service
        })
        .catch((error) => {
          console.error("Error details:", error.response?.data);
          this.errorMessage = error.response?.data?.message || "Failed to add service";
        });
    },

    clearForm() {
      this.serviceName = "";
      this.description = "";
      this.basePrice = 1;
      this.timeRequired = "";
      this.errorMessage = "";
      this.priceError = "";
    }
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  max-width: 100%;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  margin-right: 10px;
}

.alert {
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 4px;
}

.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}

.text-danger {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

input[type="number"] {
  -moz-appearance: textfield; /* Firefox */
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
