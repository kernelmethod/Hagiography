<!-- Component summarizing a character's build -->

<script>
  import { onMount } from 'svelte';

  export let buildCode;

  let buildCodePromise = null;
  let cyberneticsModule = null;
  let mutationsModule = null;
  let attributesModule = null;
  let subtypeModule = null;

  async function parseBuildCode(buildCode) {
    const ds = new DecompressionStream('gzip');

    // Base64-decode build code and convert it into a byte array
    const bcDecoded = atob(buildCode);
    const bytes = new Uint8Array(bcDecoded.length);

    for (let i = 0; i < bytes.length; i++) {
      bytes[i] = bcDecoded.charCodeAt(i);
    }

    // Decompress blob and convert to JSON
    const blob = new Blob([bytes]);
    const decompressedStream = blob.stream().pipeThrough(ds);
    const dCode = await new Response(decompressedStream).text();
    const build = JSON.parse(dCode);

    console.log(build);
    return build;
  }

  function getModule(build, moduleName) {
    for (let i = 0; i < build.modules.length; i++) {
      const module = build.modules[i];
      if (module.moduleType.includes(moduleName))
        return module;
    }

    return null;
  }

  const getCyberneticsModule = build => getModule(build, "XRL.CharacterBuilds.Qud.QudCyberneticsModule");
  const getMutationsModule = build => getModule(build, "XRL.CharacterBuilds.Qud.QudMutationsModule");
  const getAttributesModule = build => getModule(build, "XRL.CharacterBuilds.Qud.QudAttributesModule");
  const getSubtypeModule = build => getModule(build, "XRL.CharacterBuilds.Qud.QudSubtypeModule");
</script>

<style>
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
</style>

{#await parseBuildCode(buildCode) then build}
<div class="container build-summary">
  <div class="row row-cols-3">
    <!-- Attributes -->
    <div class="col">
      <div class="row build-summary-header">
        <div class="col-md-auto">
          {#if (attributesModule = getAttributesModule(build)) !== null}
          Attributes
          {:else}
          <span class="text-error">Error</span>
          {/if}
        </div>
        <div class="col"></div>
      </div>
      {#if attributesModule !== null}
      <div class="attributes">
        <p>Strength: <span>{attributesModule.data.PointsPurchased.Strength}</span></p>
        <p>Agility: <span>{attributesModule.data.PointsPurchased.Agility}</span></p>
        <p>Toughness: <span>{attributesModule.data.PointsPurchased.Toughness}</span></p>
        <p>Intelligence: <span>{attributesModule.data.PointsPurchased.Intelligence}</span></p>
        <p>Willpower: <span>{attributesModule.data.PointsPurchased.Willpower}</span></p>
        <p>Ego: <span>{attributesModule.data.PointsPurchased.Ego}</span></p>
      </div>
      {/if}
    </div>

    <!-- Caste/calling -->
    <div class="col">
      {#if (subtypeModule = getSubtypeModule(build)) !== null}
      <p>{subtypeModule.data.Subtype}</p>
      <p>{#if cyberneticsModule !== null}True Kin{:else}Mutated Human{/if}</p>
      {:else}
      <p class="text-error">Error</p>
      {/if}
    </div>

    <!-- Mutations/cybernetics -->
    <div class="col">
      <div class="row build-summary-header">
        <div class="col-md-auto">
          {#if (cyberneticsModule = getCyberneticsModule(build)) !== null}
          Cybernetics
          {:else if (mutationsModule = getMutationsModule(build)) !== null}
          Mutations
          {:else}
          <span class="text-error">Error</span>
          {/if}
        </div>
        <div class="col"></div>
      </div>
      {#if cyberneticsModule !== null}
      {#each cyberneticsModule.data.selections as cyb, _}
      <p>{cyb.Cybernetic}</p>
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
