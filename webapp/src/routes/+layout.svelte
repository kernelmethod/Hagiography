<script>
  import bootstrapCss from 'bootstrap/dist/css/bootstrap.min.css?url';
  import bootstrapSrc from 'bootstrap/dist/js/bootstrap.min.js?url';

  import Navbar from "$components/Navbar.svelte";
</script>

<svelte:head>
  <link rel="stylesheet" href={bootstrapCss}>
  <script src={bootstrapSrc}></script>
</svelte:head>

<Navbar />

<div class="container">
  <slot />

  <footer>
    <a href="/about">About</a>
  </footer>
</div>
