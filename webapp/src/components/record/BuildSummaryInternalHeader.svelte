<style lang="postcss">
  .build-summary-header {
    color: var(--qudcolor-W);
    border-color: var(--qudcolor-K);
  }
</style>

<div class="flex-auto flex flex-row items-center build-summary-header w-100">
  <div class="self-stretch border-inherit lg:border-l-2"></div>
  <div class="border-inherit max-lg:grow max-lg:border-t-2"></div>
  <div class="px-2 text-lg">
    <slot />
  </div>
  <div class="border-inherit max-lg:grow lg:flex-auto border-t-2 lg:border-r-2"></div>
  <div class="border-inherit self-stretch lg:border-r-2"></div>
</div>
