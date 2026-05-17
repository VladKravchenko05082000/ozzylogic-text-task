<script setup lang="ts" generic="TRow extends object">
export interface TableColumn {
  key: string;
  label: string;
  align?: "left" | "right";
  tdClass?: string;
}

defineProps<{
  columns: TableColumn[];
  rows: TRow[];
  rowClass?: string;
  compact?: boolean;
}>();
</script>

<template>
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead class="bg-secondary/50 border-b border-border">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            :class="[
              'px-4 py-2.5 text-xs font-medium uppercase tracking-wide text-muted-foreground',
              col.align === 'right' ? 'text-right' : 'text-left',
            ]"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-border">
        <tr v-for="(row, i) in rows" :key="i" :class="rowClass">
          <td
            v-for="col in columns"
            :key="col.key"
            :class="[
              'px-4',
              compact ? 'py-2.5' : 'py-3',
              col.align === 'right' ? 'text-right tabular-nums' : '',
              col.tdClass,
            ]"
          >
            <slot
              :name="`cell-${col.key}`"
              :row="row"
              :value="(row as Record<string, unknown>)[col.key]"
            >
              {{ (row as Record<string, unknown>)[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
