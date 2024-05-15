<script>
  import '../app.css';
  import 'bootstrap-icons/font/bootstrap-icons.min.css';

  import Navbar from "$components/Navbar.svelte";
</script>

<Navbar />

<div class="flex justify-center">
  <div class="container">
    <slot />

    <footer>
      <a href="/about">About</a>
    </footer>
  </div>
</div>
