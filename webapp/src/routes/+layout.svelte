<script>
  import Navbar from "$components/Navbar.svelte";
</script>

<Navbar />

<div class="container">
  <slot />

  <footer>
    <a href="/about">About</a>
  </footer>
</div>
