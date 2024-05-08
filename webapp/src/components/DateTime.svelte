<!-- Read a date and time from a string -->
<script>
  export let spec;

  function parseDate(date) {
    return (new Date(Date.parse(date))).toLocaleString();
  }
</script>

<span>
  {parseDate(spec)}
</span>
