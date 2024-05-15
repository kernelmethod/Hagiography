<script>
  import HeroIcon from "$components/HeroIcon.svelte";
  import RecordTable from "$components/RecordTable.svelte";
</script>

<main>
  <div class="flex justify-center">
    <HeroIcon --height="128px" />
  </div>
  <div class="flex justify-center">
    <h1 class="text-3xl underline">
      Welcome to <b>Hagiography</b>!
    </h1>
  </div>

  <p>Live and drink.</p>

  <RecordTable />
</main>
