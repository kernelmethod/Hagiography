<style>
  * {
    color: var(--qudcolor-W);
    font-style: italic;
  }

  hr {
    border: 2px solid var(--qudcolor-W);
  }

  .row {
    margin-top: 1em;
    margin-bottom: 1em;
  }
</style>

<div class="row">
  <div class="col col-lg-1">
    <hr>
  </div>
  <div class="col col-md-auto align-middle">
    <slot />
  </div>
  <div class="col">
    <hr>
  </div>
</div>
