<!-- Read a date and time from a string -->
<script>
  export let spec;

  function parseDate(date) {
    let d = new Date(Date.parse(date));
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toLocaleString();
  }
</script>

<span>
  {parseDate(spec)}
</span>
