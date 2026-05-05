import { useState } from 'react';
import { Search, ChevronRight, ChevronLeft } from 'lucide-react';

export default function DataTable({ columns, data, onRowClick, searchable = true, pageSize = 10 }) {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [sortCol, setSortCol] = useState(null);
  const [sortDir, setSortDir] = useState('asc');

  let filtered = data || [];
  if (search && searchable) {
    filtered = filtered.filter(row =>
      columns.some(col => {
        const val = typeof col.accessor === 'function' ? col.accessor(row) : row[col.accessor];
        return String(val || '').toLowerCase().includes(search.toLowerCase());
      })
    );
  }

  if (sortCol !== null) {
    const col = columns[sortCol];
    filtered = [...filtered].sort((a, b) => {
      const va = typeof col.accessor === 'function' ? col.accessor(a) : a[col.accessor];
      const vb = typeof col.accessor === 'function' ? col.accessor(b) : b[col.accessor];
      if (va < vb) return sortDir === 'asc' ? -1 : 1;
      if (va > vb) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
  }

  const totalPages = Math.ceil(filtered.length / pageSize);
  const paged = filtered.slice(page * pageSize, (page + 1) * pageSize);

  return (
    <div>
      {searchable && (
        <div className="relative mb-4">
          <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="بحث..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(0); }}
            className="input-field pr-10"
          />
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200">
              {columns.map((col, i) => (
                <th
                  key={i}
                  className="text-right py-3 px-4 font-semibold text-gray-600 cursor-pointer hover:text-gray-900"
                  onClick={() => { setSortCol(i); setSortDir(sortCol === i && sortDir === 'asc' ? 'desc' : 'asc'); }}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.length === 0 ? (
              <tr><td colSpan={columns.length} className="text-center py-8 text-gray-400">لا توجد بيانات</td></tr>
            ) : (
              paged.map((row, i) => (
                <tr
                  key={i}
                  className={`border-b border-gray-50 hover:bg-gray-50 transition-colors ${onRowClick ? 'cursor-pointer' : ''}`}
                  onClick={() => onRowClick?.(row)}
                >
                  {columns.map((col, j) => (
                    <td key={j} className="py-3 px-4">
                      {col.render ? col.render(row) : (typeof col.accessor === 'function' ? col.accessor(row) : row[col.accessor])}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
          <span>عرض {page * pageSize + 1}-{Math.min((page + 1) * pageSize, filtered.length)} من {filtered.length}</span>
          <div className="flex gap-2">
            <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="p-1 hover:bg-gray-100 rounded disabled:opacity-30">
              <ChevronRight className="w-5 h-5" />
            </button>
            <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1} className="p-1 hover:bg-gray-100 rounded disabled:opacity-30">
              <ChevronLeft className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
