<script>
  import Navbar from "$components/Navbar.svelte";
</script>

<Navbar />

<div class="container">
  <main>
    <slot />
  </main>

  <footer>
    <a href="/about">About</a>
  </footer>
</div>
