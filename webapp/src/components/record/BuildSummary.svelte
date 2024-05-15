<!-- Component summarizing a character's build -->

<script>
  import { parseBuildCode, CYBERNETIC_MAP, SUBTYPE_MAP } from '$js/BuildCodes.jsx';
  import { onMount } from 'svelte';

  import ColorizedText from '$components/ColorizedText.svelte';
  import GameTile from '$components/GameTile.svelte';

  export let buildCode;

  let cyberneticsModule = null;
  let mutationsModule = null;
  let attributesModule = null;
  let subtypeModule = null;

  let subtype = null;

  let buildParsePromise = null;

  function getModule(build, moduleName) {
    for (let i = 0; i < build.modules.length; i++) {
      const module = build.modules[i];
      if (module.moduleType.includes(moduleName))
        return module;
    }

    return null;
  }

  async function getBuild() {
    const build = await parseBuildCode(buildCode);
    cyberneticsModule = build.getCyberneticsModule();
    mutationsModule = build.getMutationsModule();
    attributesModule = build.getAttributesModule();
    subtypeModule = build.getSubtypeModule();

    subtype = (SUBTYPE_MAP[subtypeModule.data.Subtype] || (() => null))();
    return build;
  }

  onMount(() => {
    buildParsePromise = getBuild();
  });
</script>

<style lang="postcss">
  .build-summary-header {
    color: var(--qudcolor-W);
  }

  .build-summary {
    margin-bottom: 2em;
  }

  .build-summary .col {
    padding: 0 1em 0 1em;
  }

  .build-summary-header {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 1em;

    border-style: solid;
    border-width: 0 3px 0 3px;
    border-color: var(--qudcolor-K);
  }

  .build-summary-header > div:nth-of-type(2) {
    border-width: 3px 3px 0 0;
    border-color: var(--qudcolor-K);
    border-style: solid;
  }

  p {
    margin: 0;
  }

  .attributes span {
    float: right;
  }

  .subtype-tile {
    height: 60%;
  }
</style>

{#if buildParsePromise !== null}
{#await buildParsePromise then build}
<div class="container build-summary">
  <div class="grid grid-cols-3">
    <!-- Attributes -->
    <div>
      <div class="flex flex-row build-summary-header">
        <div class="px-2 text-lg">
          {#if attributesModule !== null}
          Attributes
          {:else}
          <span class="text-error">Error</span>
          {/if}
        </div>
        <div class="flex-auto"></div>
      </div>
      {#if attributesModule !== null && subtype !== null}
      <div class="attributes">
        <p>Strength: <span>{attributesModule.data.PointsPurchased.Strength + subtype.Strength()}</span></p>
        <p>Agility: <span>{attributesModule.data.PointsPurchased.Agility + subtype.Agility()}</span></p>
        <p>Toughness: <span>{attributesModule.data.PointsPurchased.Toughness + subtype.Toughness()}</span></p>
        <p>Intelligence: <span>{attributesModule.data.PointsPurchased.Intelligence + subtype.Intelligence()}</span></p>
        <p>Willpower: <span>{attributesModule.data.PointsPurchased.Willpower + subtype.Willpower()}</span></p>
        <p>Ego: <span>{attributesModule.data.PointsPurchased.Ego + subtype.Ego()}</span></p>
      </div>
      {/if}
    </div>

    <!-- Caste/calling -->
    <div class="px-8">
      {#if subtypeModule !== null}
      {#if subtype !== null}
      <div class="flex justify-center subtype-tile">
        <GameTile --height2="60%" tile={subtype.getTile()} />
      </div>
      {:else}
      <p class="text-error">Error: unknown subtype {subtypeModule.data.Subtype}</p>
      {/if}
      <p>{subtypeModule.data.Subtype}</p>
      <p>{#if cyberneticsModule !== null}True Kin{:else}Mutated Human{/if}</p>
      {:else}
      <p class="text-error">Error: could not find XRL.CharacterBuilds.Qud.QudSubtypeModule</p>
      {/if}
    </div>

    <!-- Mutations/cybernetics -->
    <div>
      <div class="flex flex-row build-summary-header">
        <div class="px-2 text-lg">
          {#if cyberneticsModule !== null}
          Cybernetics
          {:else if mutationsModule !== null}
          Mutations
          {:else}
          <span class="text-error">Error</span>
          {/if}
        </div>
        <div class="flex-auto"></div>
      </div>
      {#if cyberneticsModule !== null}
      {#each cyberneticsModule.data.selections as cyb, _}
        {#if CYBERNETIC_MAP[cyb.Cybernetic] !== undefined}
        <p>
          <ColorizedText text={CYBERNETIC_MAP[cyb.Cybernetic]} />
        </p>
        {:else}
        <p class="text-error">
          Unknown cybernetic {cyb.Cybernetic}
        </p>
        {/if}
      {/each}
      {:else if mutationsModule !== null}
      {#each mutationsModule.data.selections as mut, _}
      <p>{mut.Mutation} {#if mut.Count > 1} x{mut.Count}{/if}</p>
      {/each}
      {/if}
    </div>
  </div>
</div>
{/await}
{/if}
