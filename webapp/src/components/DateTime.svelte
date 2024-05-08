<!-- Read a date and time from a string -->
<script>
  export let timestamp;

  function parseDate(ts) {
    return (new Date(1000 * ts)).toLocaleString();
  }
</script>

<span>
  {parseDate(timestamp)}
</span>
