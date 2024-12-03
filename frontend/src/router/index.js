import Vue from "vue";
import VueRouter from "vue-router";
import CustomerSignUp from "../components/CustomerSignup.vue";
import ServiceProfessionalSignUp from "../components/ServiceProfessionalSignup.vue";
import UserLogin from "../components/UserLogin.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";
import UserDashboard from "@/components/UserDashboard.vue";
import ServiceProviderDashboard from "@/components/ServiceProviderDashboard.vue";
import AddService from "@/components/AddService.vue";
import ListAllUsers from "@/components/ListAllUsers.vue";
import ListAllProfessionals from "@/components/ListAllProfessionals.vue";
import SearchServiceRequest from "@/components/SearchServiceRequest.vue";
import SummaryCharts from "@/components/SummaryCharts.vue";
import ListAllServices from "@/components/ListAllServices.vue";

Vue.use(VueRouter);

const routes = [
  { 
    path: "/signup", 
    component: CustomerSignUp, 
    name: 'customer-signup',
    meta: { requiresGuest: true }
  },
  { 
    path: "/signup/service-provider", 
    component: ServiceProfessionalSignUp, 
    name: 'service-provider-signup',
    meta: { requiresGuest: true }
  },
  { 
    path: "/login", 
    component: UserLogin, 
    name: 'login',
    meta: { requiresGuest: true }
  },
  { 
    path: "/admin", 
    component: AdminDashboard, 
    name: 'AdminDashboard',
    meta: { requiresAuth: true, role: 'admin' }
  },
  { 
    path: "/admin/summary", 
    component: SummaryCharts, 
    name: 'SummaryCharts',
    meta: { requiresAuth: true, role: 'admin' }
  },
  { 
    path: "/admin/service", 
    component: AddService, 
    name: 'create-service',
    meta: { requiresAuth: true, role: 'admin' }
  },
  { 
    path: "/user", 
    component: UserDashboard, 
    name: 'UserDashboard',
    meta: { requiresAuth: true, role: 'customer' }
  },
  { 
    path: "/serviceprovider", 
    component: ServiceProviderDashboard, 
    name: 'ServiceProviderDashboard',
    meta: { requiresAuth: true, role: 'service_professional' }
  },
  { 
    path: '/admin/search', 
    component: SearchServiceRequest, 
    name: 'search-service-request',
    meta: { requiresAuth: true, role: 'admin' }
  },
  { 
    path: '/admin/users', 
    component: ListAllUsers, 
    name: 'ListAllUsers',
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/service-professionals',
    component: ListAllProfessionals,
    name: 'list-professionals',
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/listservices',
    name: 'listallservices',
    component: ListAllServices,
    meta: { requiresAuth: true, role: 'admin' }
  },
  // Redirect any unknown routes to login
  {
    path: '*',
    redirect: '/login'
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
  scrollBehavior() {
    return { x: 0, y: 0 }  // Scroll to top on route change
  }
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresGuest = to.matched.some(record => record.meta.requiresGuest);
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');

  // Debug logs
  console.log('Route:', to.path);
  console.log('Token:', token);
  console.log('User Role:', userRole);
  console.log('Requires Auth:', requiresAuth);
  console.log('Requires Guest:', requiresGuest);

  if (requiresAuth && !token) {
    // If route requires auth and no token is present
    console.log('No token, redirecting to login');
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    });
  } else if (requiresGuest && token) {
    // If route is for guests only and user is logged in
    console.log('User is logged in, redirecting to dashboard');
    next(getDashboardByRole(userRole));
  } else if (requiresAuth && to.meta.role && to.meta.role !== userRole) {
    // If user doesn't have required role
    console.log('Wrong role, redirecting to appropriate dashboard');
    next(getDashboardByRole(userRole));
  } else {
    // All checks passed
    console.log('Proceeding to route');
    next();
  }
});

function getDashboardByRole(role) {
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
}

// Add this to handle navigation duplicates globally
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => {
    if (err.name !== 'NavigationDuplicated') {
      throw err;
    }
  });
};

export default router;
