<!-- Component summarizing a character's build -->

<script>
  import { parseBuildCode, CYBERNETIC_MAP, SUBTYPE_MAP } from '$js/BuildCodes.jsx';
  import { onMount } from 'svelte';

  import BuildSummaryInternalHeader from '$components/record/BuildSummaryInternalHeader.svelte';
  import ClipboardWidget from '$components/ClipboardWidget.svelte';
  import ColorizedText from '$components/ColorizedText.svelte';
  import GameTile from '$components/GameTile.svelte';
  import Modal from '$components/Modal.svelte';

  export let buildCode;

  let buildCodeModal = null;

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
  <div class="grid max-lg:grid-cols-2 max-lg:grid-rows-2 lg:grid-cols-3 border-inherit">
    <!-- Attributes -->
    <div class="max-lg:row-start-2 col-span-1 px-2">
      <BuildSummaryInternalHeader>
        {#if attributesModule !== null}
        Attributes
        {:else}
        <span class="text-error">Error</span>
        {/if}
      </BuildSummaryInternalHeader>
      {#if attributesModule !== null && subtype !== null}
      <div class="attributes px-2">
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
    <div class="max-lg:row-start-1 max-lg:col-span-2 max-lg:border-0 max-lg:mb-8">
      {#if subtypeModule !== null}
      {#if subtype !== null}
      <div class="flex justify-center subtype-tile">
        <GameTile --height2="60%" tile={subtype.getTile()} />
      </div>
      {:else}
      <p class="text-error">Error: unknown subtype {subtypeModule.data.Subtype}</p>
      {/if}
      <div class="text-center">
        <p>{subtypeModule.data.Subtype}</p>
        <p>{#if cyberneticsModule !== null}True Kin{:else}Mutated Human{/if}</p>
        {#if buildCodeModal !== null}
        <p>
          <button type="button" class="px-2 hover:bg-emerald-900 rounded-md" on:click={() => buildCodeModal.show()}>
            <i class="bi-clipboard"></i> Show build code
          </button>
        </p>
        {/if}
      </div>
      {:else}
      <p class="text-error">Error: could not find XRL.CharacterBuilds.Qud.QudSubtypeModule</p>
      {/if}
    </div>

    <!-- Mutations/cybernetics -->
    <div class="max-lg:row-start-2 max-lg:border-l-2 col-span-1 border-qudcolor-K px-2">
      <BuildSummaryInternalHeader>
        {#if cyberneticsModule !== null}
        Cybernetics
        {:else if mutationsModule !== null}
        Mutations
        {:else}
        <span class="text-error">Error</span>
        {/if}
      </BuildSummaryInternalHeader>
      <div class="px-2">
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
</div>
{/await}
{/if}

<Modal bind:this={buildCodeModal} --width="max(60vw, 500px)">
  <div slot="modalHeader">
    Build code
  </div>

  <div slot="modalBody">
    <ClipboardWidget>
      {buildCode}
    </ClipboardWidget>
  </div>
</Modal>
