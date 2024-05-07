<script>
  import { onMount } from 'svelte';
  import { COLORMAP } from '$js/Color.jsx';

  let canvas;

  export let tileURL;
  export let renderString = " ";
  export let colorString;
  export let detailColor;
  export let tileColor = null;
  export let hflip = false;
  export let vflip = false;

  onMount(() => {
    const img = new Image();
    img.src = tileURL;

    const ctx = canvas.getContext('2d');

    if (tileColor in COLORMAP) {
      let color = COLORMAP[tileColor];
      color = "#" + color[0].toString(16) + color[1].toString(16) + color[2].toString(16);
      canvas.style.setProperty("background-color", color);
    }

    if (hflip) {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }
    if (vflip) {
      ctx.translate(0, canvas.height);
      ctx.scale(1, -1);
    }

    img.onload = () => {
      ctx.drawImage(img, 0, 0);
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      const primary = COLORMAP[colorString];
      const secondary = COLORMAP[detailColor]; 

      for (let i = 0; i < data.length; i += 4) {
        let weight = data[i] / 255;

        for (let j = 0; j < 3; j++) {
          // Weighted average of color channels for primary and
          // detail colors.
          const pixelColor = (1 - weight) * primary[j] + weight * secondary[j];
          data[i + j] = pixelColor;
        }
      }
      ctx.putImageData(imageData, 0, 0);
    };
  });
</script>

<style>
  canvas {
    height: var(--height, 100%);
    image-rendering: crisp-edges;
  }
</style>

<canvas bind:this={canvas} width=16 height=24></canvas>
