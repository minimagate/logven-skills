// Both the editable report and read-only dashboard import this module.
export function mount(report, options) {
  let draft = {...report.config};
  return {
    change(key, value) { draft[key] = value; if (options.live) options.save(draft); },
    addColumn(column) { draft.columns.push(column); },
    removeColumn(index) { draft.columns.splice(index, 1); },
    copy() { return options.create({...report, config: draft}); }
  };
}
