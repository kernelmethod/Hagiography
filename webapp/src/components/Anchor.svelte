<script>
  export let name;
</script>

<span id="{encodeURIComponent(name)}">
  <slot />
</span>
