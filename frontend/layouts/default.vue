<template>
  <Notification>
    <div class="fwh main_div">
      <Header />
      <div class="content">
        <slot></slot>
      </div>
    </div>
  </Notification>
</template>

<script setup>
import Header from "./header.vue";
import Notification from "./notification.vue";
</script>

<style scoped>
.main_div {
  background: var(--bg-grad);
  width: 100%;
  min-height: 100vh;
}
.content {
  padding: calc(var(--padding-content-height) + var(--header-height))
    var(--padding-content-width);
  width: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
