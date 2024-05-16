<!-- Read a date and time from a string -->
<script>
  export let timestamp;
  export let showDelta = false;

  function getDelta(date) {
    const currentTime = Date.now();
    const seconds = (currentTime - date) / 1000;

    if (seconds < 60)
      return pluralTime(seconds, 'second');

    const minutes = seconds / 60;
    if (minutes < 60)
      return pluralTime(minutes, 'minute');

    const hours = minutes / 60;
    if (hours < 24)
      return pluralTime(hours, 'hour');

    const days = hours / 24;
    if (days < 7)
      return pluralTime(days, 'day');

    return new Date(currentTime).toLocaleDateString();
  }

  function pluralTime(n, unit) {
    n = Math.floor(n);

    if (n > 1)
      unit = unit + 's';

    return `${n} ${unit} ago`;
  }

  let date = new Date(1000 * timestamp);

  if (showDelta) {
    date = getDelta(date);
  }
  else {
    date = date.toLocaleString();
  }
</script>

<span>{date}</span>
