<style lang="postcss">
  * {
    color: var(--qudcolor-W);
    font-style: italic;
  }

  div {
    align-items: center;
    border-color: var(--qudcolor-W);
  }

  hr {
    border: 2px solid var(--qudcolor-W);
  }
</style>

<div class="flex flex-row my-4">
  <div class="w-14 align-middle inline-block border-t-2"></div>
  <div class="px-4 text-xl">
    <slot />
  </div>
  <div class="flex-auto border-t-2"></div>
</div>
