<template>
  <main>
    <h1>Ingestion</h1>
    <div class="grid-cols-2 gap-2 grid h-40">
      <CardChoice
        title="Programatic"
        description="Submit samples to the API from your own application."
        to="ingestion/programatic"
        disabled
      />
      <CardChoice
        title="Manual"
        description="Use the UI to upload a spreadsheet of samples."
        to="ingestion/manual"
      />
    </div>
  </main>
</template>
