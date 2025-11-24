'use client';

import { FilterOption } from '@/types';

interface FiltersBarProps {
  filters: FilterOption[];
  onToggleFilter: (index: number) => void;
}

export default function FiltersBar({ filters, onToggleFilter }: FiltersBarProps) {
  return (
    <div className="filters-bar">
      <p>Quick filters:</p>
      <div className="filters-chips">
        {filters.map((filter, index) => (
          <button
            key={`${filter.type}-${filter.value}`}
            className={`filter-chip ${filter.active ? 'active' : ''}`}
            onClick={() => onToggleFilter(index)}
            type="button"
          >
            {filter.value}
          </button>
        ))}
      </div>
    </div>
  );
}

