<template>
  <WrapperModal v-if="isOpenModal" @closeModal="close">
    <div v-if="type === 1" class="block">
      <h2>Change Username to {{ username }}</h2>
      <p style="color: var(--main-color70)">To confirm, enter your password</p>
      <h3>Password</h3>
      <CInput
        class="input"
        type="password"
        placeholder="Enter password"
        v-model="oldPassword"
      />
      <CButton @click="saveChanges">Save Changes</CButton>
    </div>
    <div class="block" v-else>
      <h2>Change Password:</h2>
      <p style="color: var(--main-color70)">
        To confirm, enter your old password
      </p>
      <h3>Old Password</h3>
      <CInput
        class="input"
        type="password"
        placeholder="Enter old password"
        v-model="oldPassword"
      />
      <h3>New Password</h3>
      <CInput
        class="input"
        type="password"
        placeholder="Enter new password"
        v-model="newPassword"
      />
      <CButton @click="saveChanges">Change Password</CButton>
    </div>
  </WrapperModal>

  <div class="person-information">
    <h1>Personal Account</h1>

    <div class="block">
      <h3>Email</h3>
      <CInput
        class="input"
        placeholder="Enter email"
        v-model="information.email"
        :readonly="true"
      />
    </div>
    <div class="block">
      <h3>Username</h3>
      <CInput class="input" placeholder="Enter username" v-model="username" />
    </div>
    <CButton @click="open(1)">Save Changes</CButton>
    <CButton @click="open(2)">Change Password</CButton>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from "vue";
import { useNuxtApp } from "#app";

const { $api } = useNuxtApp();
const information = ref({});
const username = ref("");
const oldPassword = ref("");
const newPassword = ref("");

const isOpenModal = ref(false);
const type = ref(0);

function open(newValue) {
  type.value = newValue;
  isOpenModal.value = true;
}

function close() {
  isOpenModal.value = false;
  // Clear passwords when closing the modal
  oldPassword.value = "";
  newPassword.value = "";
}

async function saveChanges() {
  try {
    const endpoint =
      type.value === 1
        ? `api/v1/user/me_update?username=${username.value}&old_password=${oldPassword.value}`
        : `api/v1/user/me_update?old_password=${oldPassword.value}&password=${newPassword.value}`;

    const responseInformation = await $api.put(
      endpoint,
      {},
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    createNotification(`Changes saved successfully!`, "success");
    close(); // Close the modal after saving changes
  } catch (error) {
    console.error("Error loading data", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function fetchData() {
  try {
    const responseInformation = await $api.get(`api/v1/user/me`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    information.value = responseInformation.data;
    username.value = information.value.username;
  } catch (error) {
    console.error("Error loading data", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

onMounted(() => {
  fetchData();
  fetch();
});

let createNotification;

function fetch() {
  createNotification = inject("createNotification");
}
</script>

<style scoped>
.person-information {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.block {
  align-items: center;
  justify-content: center;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input {
  width: 250px;
}
</style>
