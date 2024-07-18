<template>
  <div>
    <h1>Ingestion</h1>
    <div class="grid-cols-2 gap-2 grid h-40">
      <ButtonCard
        class="w-full"
        to="/ingestion/programatic"
      >
        <div>
          Programatic
          <p class="text-sm text-gray-600">
            Submit samples to the API from your own application.
          </p>
        </div>
      </ButtonCard>
      <ButtonCard
        class="w-full"
        to="/ingestion/manual"
      >
        <div>
          Manual
          <p class="text-sm text-gray-600">
            Use the UI to upload a spreadsheet of samples.
          </p>
        </div>
      </ButtonCard>
    </div>
  </div>
</template>
