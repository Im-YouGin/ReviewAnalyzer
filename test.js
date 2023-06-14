const root = document.getElementById("app");


const ExchangeAssetsInGroupTable = {
    selectedRow: null,
    selectedAsset: null,
    selectedPeriod: null,
    selectedGroupAsset: null,
    startDate: '',
    endDate: '',
    searchQuery: '',
    view: ({attrs}) => {
        const data = attrs.data;

        // Group data by exchange_asset
        const groupedData = data.reduce((grouped, item) => {
            const key = `${item.exchange_asset.ticker}${item.exchange_asset.asset_isin}${item.exchange_asset.exchange_mic}`;

            if (!grouped[key]) {
                grouped[key] = {
                    exchange_asset: item.exchange_asset,
                    periods: []
                };
            }

            grouped[key].periods.push({
                start: item.start_date,
                end: item.end_date,
                id: item.id
            });

            return grouped;
        }, {});

        // Convert object to array
        const groupedDataArray = Object.values(groupedData);

        return  m('.d-flex.flex-column', {
            oncreate: vnode => {
                ExchangeAssetsInGroupTable.clickOutsideListener = (e) => {
                    if (!e.target.closest('.ignore-outer-click') && !e.target.closest('.table')) {
                        console.log('set to null');
                        ExchangeAssetsInGroupTable.selectedRow = null;
                        ExchangeAssetsInGroupTable.selectedAsset = null;
                        ExchangeAssetsInGroupTable.selecteGroupAsset = null;
                        ExchangeAssetsInGroupTable.selectedPeriod = null;
                        m.redraw();
                    }
                };
                document.addEventListener('click', ExchangeAssetsInGroupTable.clickOutsideListener);
            },
            onremove: vnode => {
                document.removeEventListener('click', ExchangeAssetsInGroupTable.clickOutsideListener);
            }
        }, [
            m('h5', 'Assets in this group'),
                   m('.input-group.mb-2', [
                m('input.form-control', {
                    style: 'font-size: 0.8rem;',
                    type: 'text',
                    placeholder: 'Search',
                    oninput: e => {
                        ExchangeAssetsInGroupTable.searchQuery = e.target.value;
                    },
                    value: ExchangeAssetsInGroupTable.searchQuery
                }),
                m('.input-group-append', m('button.btn.btn-outline-secondary', {
                    style: 'font-size: 0.8rem;',
                    type: 'button',
                    onclick: (e) => {
                        Main.fetchExistingExchangeAssets().finally(m.redraw)
                    }
                }, 'Search'))
            ]),
            m('div.table-responsive', {style: 'max-height: 300px;'}, [
                m('table.table.table-hover', [
                    m('thead.thead-sticky.table-primary', [
                        m('tr', [
                            m('th', 'Ticker'),
                            m('th', 'ISIN'),
                            m('th', 'MIC'),
                            m('th', 'Start Date'),
                            m('th', 'End Date'),
                            m('th', 'Action')
                        ])
                    ]),
                    m('tbody',
                        {
                            ondragover: (e) => {
                                e.preventDefault(); // Allow the drop
                            },
                            ondrop: (e) => {
                                e.preventDefault();
                                const asset = JSON.parse(e.dataTransfer.getData('application/json'));
                                Main.addGroupExchangeAsset(asset);
                            }
                        },
                        groupedDataArray.map((obj, rowIndex) =>
                            obj.periods.map((period, index) => m('tr', {
                                class: ExchangeAssetsInGroupTable.selectedRow === rowIndex ? 'selected' : '',
                                onclick: () => {
                                    ExchangeAssetsInGroupTable.selectedRow = `${rowIndex}_${index}`;
                                    ExchangeAssetsInGroupTable.startDate = '';
                                    ExchangeAssetsInGroupTable.endDate = '';
                                    ExchangeAssetsInGroupTable.selectedAsset = obj.exchange_asset.id;
                                    ExchangeAssetsInGroupTable.selecteGroupAsset = period.id;

                                    console.log('set value');
                                }
                            }, [
                                m('td', index === 0 && obj.exchange_asset.ticker),
                                m('td', index === 0 && obj.exchange_asset.asset_isin),
                                m('td', index === 0 && obj.exchange_asset.exchange_mic),
                                m('td', period.start || '-'),
                                m('td', period.end || '-'),
                                m('td',
                                    ExchangeAssetsInGroupTable.selectedRow === `${rowIndex}_${index}`
                                        ? [
                                            m('button.btn.btn-primary', {
                                                style: 'padding: 0 5px; margin-right: 28px',
                                                onclick: (e) => {
                                                    e.stopPropagation();

                                                    ExchangeAssetsInGroupTable.startDate = period.start;
                                                    ExchangeAssetsInGroupTable.endDate = period.end;

                                                    $('#editPeriodModal').modal('show');
                                                }
                                            }, m('span.fas.fa-edit', {style: 'font-size: 0.8rem'})),
                                            m('button.btn.btn-danger', {
                                                style: 'padding: 0 5px',

                                                onclick: (e) => {
                                                    e.stopPropagation();
                                                    $('#deleteModal').modal('show');
                                                }
                                            }, m('span.fas.fa-trash', {style: 'font-size: 0.8rem'}))
                                        ]
                                        : (obj.periods.length === index + 1) && m('button.btn.btn-primary', {
                                        style: 'font-size: 0.8rem; padding: 0.15rem 0.3rem',
                                        onclick: (e) => {
                                            e.stopPropagation();
                                            ExchangeAssetsInGroupTable.selectedAsset = obj.exchange_asset.id;
                                            $('#addPeriodModal').modal('show');
                                        }
                                    }, 'Add Period')
                                )
                            ]))
                        )
                    )
                ]),
            ]),
            // Add Period Modal
            m('div#addPeriodModal.modal.fade.ignore-outer-click', [
                m('div.modal-dialog', [
                    m('div.modal-content', [
                        m('div.modal-header', [
                            m('h5.modal-title', 'Add Period'),
                            m('button.btn-close', {'data-bs-dismiss': 'modal'})
                        ]),
                        m('div.modal-body', [
                            m('h6', 'Start date'),
                            m('input.form-control',
                                {
                                    type: 'date',
                                    value: ExchangeAssetsInGroupTable.startDate,
                                    onchange: (e) => {
                                        ExchangeAssetsInGroupTable.startDate = e.target.value;
                                    }
                                })
                        ]),
                        m('div.modal-footer', [
                            m('button.btn.btn-primary', {
                                onclick: () => {
                                    console.log(ExchangeAssetsInGroupTable.selectedAsset,)
                                    Main.addGroupExchangeAsset({
                                        exchange_asset: ExchangeAssetsInGroupTable.selectedAsset,
                                        start_date: ExchangeAssetsInGroupTable.startDate
                                    }).then(() => $('#addPeriodModal').modal('hide'));
                                }
                            }, 'Add')
                        ])
                    ])
                ])
            ]),
            // Edit period modal:
            m('div#editPeriodModal.modal.fade.ignore-outer-click', [
                m('div.modal-dialog', [
                    m('div.modal-content', [
                        m('div.modal-header', [
                            m('h5.modal-title', 'Edit Period'),
                            m('button.btn-close', {'data-bs-dismiss': 'modal'})
                        ]),
                        m('div.modal-body', [
                            m('h6', 'Start date'),
                            m('input.form-control',
                                {
                                    type: 'date',
                                    value: ExchangeAssetsInGroupTable.startDate,
                                    onchange: (e) => {
                                        ExchangeAssetsInGroupTable.startDate = e.target.value;
                                    }
                                }),
                            m('h6.mt-3', 'End date'),
                            m('input.form-control',
                                {
                                    type: 'date',
                                    value: ExchangeAssetsInGroupTable.endDate,
                                    onchange: (e) => {
                                        ExchangeAssetsInGroupTable.endDate = e.target.value;
                                    }
                                }),
                        ]),
                        m('div.modal-footer', [
                            m('button.btn.btn-primary', {
                                onclick: () => {
                                    Main.patchGroupExchangeAsset({
                                        id: ExchangeAssetsInGroupTable.selecteGroupAsset,
                                        data: {
                                            start_date: ExchangeAssetsInGroupTable.startDate,
                                            end_date: ExchangeAssetsInGroupTable.endDate
                                        }
                                    }).then(() => $('#editPeriodModal').modal('hide'));
                                }
                            }, 'Save Changes')
                        ])
                    ])
                ])
            ]),
            // Delete Modal
            m('div#deleteModal.modal.fade.ignore-outer-click', [
                m('div.modal-dialog', [
                    m('div.modal-content', [
                        m('div.modal-header', [
                            m('h5.modal-title', 'Delete Period'),
                            m('button.btn-close', {'data-bs-dismiss': 'modal'})
                        ]),
                        m('div.modal-body', [
                            m('p', 'Are you sure you want to delete this period?'),
                        ]),
                        m('div.modal-footer', [
                            m('button.btn.btn-danger', {
                                onclick: () => {
                                    Main.deleteGroupExchangeAsset(ExchangeAssetsInGroupTable.selecteGroupAsset).then(() => $('#deleteModal').modal('hide'));
                                }
                            }, 'Delete')
                        ])
                    ])
                ])
            ]),
        ])
    }
};


const AssetGroupsInGroupTable = {
    selectedRow: null,
    selectedAssetGroup: null,
    selectedPeriod: null,
    selectedGroupAssetGroup: null,
    startDate: '',
    endDate: '',
    searchQuery: '',
    view: ({attrs}) => {
        const data = attrs.data;

        // Group data by exchange_asset
        const groupedData = data.reduce((grouped, item) => {
            const key = item.child_exchange_asset_group.name;

            if (!grouped[key]) {
                grouped[key] = {
                    childGroup: item.child_exchange_asset_group,
                    periods: []
                };
            }

            grouped[key].periods.push({
                start: item.start_date,
                end: item.end_date,
                id: item.id
            });

            return grouped;
        }, {});

        // Convert object to array
        const groupedDataArray = Object.values(groupedData);
        return  m('.d-flex.flex-column',
            {
                oncreate: vnode => {
                    AssetGroupsInGroupTable.clickOutsideListener = (e) => {
                        if (!e.target.closest('.ignore-outer-click') && !e.target.closest('.table')) {
                            console.log('set to null');
                            AssetGroupsInGroupTable.selectedRow = null;
                            AssetGroupsInGroupTable.selecteGroupAsset = null;
                            AssetGroupsInGroupTable.selectedGroupAssetGroup = null;
                            AssetGroupsInGroupTable.selectedPeriod = null;
                            m.redraw();
                        }
                    };
                    document.addEventListener('click', AssetGroupsInGroupTable.clickOutsideListener);
                },
                onremove: vnode => {
                    document.removeEventListener('click', AssetGroupsInGroupTable.clickOutsideListener);
                }
            }, [
                m('h5', 'Groups in this group'),
                m('.input-group.mb-2', [
                m('input.form-control', {
                    style: 'font-size: 0.8rem;',
                    type: 'text',
                    placeholder: 'Search',
                    oninput: e => {
                        AssetGroupsInGroupTable.searchQuery = e.target.value;
                    },
                    value: AssetGroupsInGroupTable.searchQuery
                }),
                m('.input-group-append', m('button.btn.btn-outline-secondary', {
                    style: 'font-size: 0.8rem;',
                    type: 'button',
                    onclick: (e) => {
                        Main.fetchGroupsExisting().finally(m.redraw)
                    }
                }, 'Search'))
            ]),
                m('div.table-responsive', {style: 'max-height: 300px;'}, [
                    m('table.table.table-hover', [
                        m('thead.thead-sticky.table-primary',
                            m('tr', [m('th', 'Name'),
                                m('th', 'Num assets'),
                                m('th', 'Start'),
                                m('th', 'End'),
                                m('th', 'Action'),])
                        ),
                        m('tbody',
                            {
                                ondragover: (e) => {
                                    e.preventDefault(); // Allow the drop
                                },
                                ondrop: (e) => {
                                    e.preventDefault();
                                    const group = JSON.parse(e.dataTransfer.getData('application/json'));
                                    Main.addGroupExchangeAssetGroup(group);
                                }
                            },
                            groupedDataArray.map((obj, rowIndex) =>
                                obj.periods.map((period, index) => m('tr', {
                                    class: AssetGroupsInGroupTable.selectedRow === rowIndex ? 'selected' : '',
                                    onclick: () => {
                                        AssetGroupsInGroupTable.selectedRow = `${rowIndex}_${index}`;
                                        AssetGroupsInGroupTable.startDate = '';
                                        AssetGroupsInGroupTable.endDate = '';
                                        AssetGroupsInGroupTable.selectedAssetGroup = obj.childGroup.id;
                                        AssetGroupsInGroupTable.selectedGroupAssetGroup = period.id;
                                        console.log(AssetGroupsInGroupTable.selectedGroupAssetGroup);
                                        console.log('set value');
                                    }
                                }, [
                                    m('td', index === 0 && obj.childGroup.name),
                                    m('td', index === 0 && obj.childGroup.num_assets),
                                    m('td', period.start || '-'),
                                    m('td', period.end || '-'),
                                    m('td',
                                        AssetGroupsInGroupTable.selectedRow === `${rowIndex}_${index}`
                                            ? [
                                                m('button.btn.btn-primary', {
                                                    style: 'padding: 0 5px; margin-right: 28px',
                                                    onclick: (e) => {
                                                        e.stopPropagation();

                                                        AssetGroupsInGroupTable.startDate = period.start;
                                                        AssetGroupsInGroupTable.endDate = period.end;

                                                        $('#editGroupPeriodModal').modal('show');
                                                    }
                                                }, m('span.fas.fa-edit', {style: 'font-size: 0.8rem',})),
                                                m('button.btn.btn-danger', {
                                                    style: 'padding: 0 5px',
                                                    onclick: (e) => {
                                                        e.stopPropagation();
                                                        $('#deleteGroupModal').modal('show');
                                                    }
                                                }, m('span.fas.fa-trash', {style: 'font-size: 0.8rem',}))
                                            ]
                                            : (obj.periods.length === index + 1) && m('button.btn.btn-primary', {
                                            style: 'font-size: 0.8rem; padding: 0.15rem 0.3rem',
                                            onclick: (e) => {
                                                e.stopPropagation();
                                                AssetGroupsInGroupTable.selectedAssetGroup = obj.childGroup.id;
                                                $('#addGroupPeriodModal').modal('show');
                                            }
                                        }, 'Add Period')
                                    )
                                ]))
                            )
                        )
                    ]),
                    // Add Period Modal
                    m('div#addGroupPeriodModal.modal.fade.ignore-outer-click', [
                        m('div.modal-dialog', [
                            m('div.modal-content', [
                                m('div.modal-header', [
                                    m('h5.modal-title', 'Add Period'),
                                    m('button.btn-close', {'data-bs-dismiss': 'modal'})
                                ]),
                                m('div.modal-body', [
                                    m('h6', 'Start date'),
                                    m('input.form-control',
                                        {
                                            type: 'date',
                                            value: AssetGroupsInGroupTable.startDate,
                                            onchange: (e) => {
                                                AssetGroupsInGroupTable.startDate = e.target.value;
                                            }
                                        })
                                ]),
                                m('div.modal-footer', [
                                    m('button.btn.btn-primary', {
                                        onclick: () => {
                                            Main.addGroupExchangeAssetGroup({
                                                child_exchange_asset_group: AssetGroupsInGroupTable.selectedAssetGroup,
                                                start_date: AssetGroupsInGroupTable.startDate
                                            }).then(() => $('#addGroupPeriodModal').modal('hide'));
                                        }
                                    }, 'Add')
                                ])
                            ])
                        ])
                    ]),
                    // Edit period modal:
                    m('div#editGroupPeriodModal.modal.fade.ignore-outer-click', [
                        m('div.modal-dialog', [
                            m('div.modal-content', [
                                m('div.modal-header', [
                                    m('h5.modal-title', 'Edit Period'),
                                    m('button.btn-close', {'data-bs-dismiss': 'modal'})
                                ]),
                                m('div.modal-body', [
                                    m('h6', 'Start date'),
                                    m('input.form-control',
                                        {
                                            type: 'date',
                                            value: AssetGroupsInGroupTable.startDate,
                                            onchange: (e) => {
                                                AssetGroupsInGroupTable.startDate = e.target.value;
                                            }
                                        }),
                                    m('h6.mt-3', 'End date'),
                                    m('input.form-control',
                                        {
                                            type: 'date',
                                            value: AssetGroupsInGroupTable.endDate,
                                            onchange: (e) => {
                                                AssetGroupsInGroupTable.endDate = e.target.value;
                                            }
                                        }),
                                ]),
                                m('div.modal-footer', [
                                    m('button.btn.btn-primary', {
                                        onclick: () => {
                                            Main.patchGroupExchangeAssetGroup({
                                                id: AssetGroupsInGroupTable.selectedGroupAssetGroup,
                                                data: {
                                                    start_date: AssetGroupsInGroupTable.startDate,
                                                    end_date: AssetGroupsInGroupTable.endDate
                                                }
                                            }).then(() => $('#editGroupPeriodModal').modal('hide'));
                                        }
                                    }, 'Save Changes')
                                ])
                            ])
                        ])
                    ]),
                    // Delete Modal
                    m('div#deleteGroupModal.modal.fade.ignore-outer-click', [
                        m('div.modal-dialog', [
                            m('div.modal-content', [
                                m('div.modal-header', [
                                    m('h5.modal-title', 'Delete Period'),
                                    m('button.btn-close', {'data-bs-dismiss': 'modal'})
                                ]),
                                m('div.modal-body', [
                                    m('p', 'Are you sure you want to delete this period?'),
                                ]),
                                m('div.modal-footer', [
                                    m('button.btn.btn-danger', {
                                        onclick: () => {
                                            Main.deleteGroupExchangeAssetGroup(AssetGroupsInGroupTable.selectedGroupAssetGroup).then(() => $('#deleteGroupModal').modal('hide'));
                                        }
                                    }, 'Delete')
                                ])
                            ])
                        ])
                    ]),
                ])
            ])
    }
};


const ExchangeAssetsTable = {
    searchQuery: '',

    view: ({attrs}) => {
        const data = attrs.data;

        return  m('.d-flex.flex-column', [
            m('h5', 'Assets'),
            m('.input-group.mb-2', [
                m('input.form-control', {
                    style: 'font-size: 0.8rem;',
                    type: 'text',
                    placeholder: 'Search',
                    oninput: e => {
                        ExchangeAssetsTable.searchQuery = e.target.value;
                    },
                    value: ExchangeAssetsTable.searchQuery
                }),
                m('.input-group-append', m('button.btn.btn-outline-secondary', {
                    style: 'font-size: 0.8rem;',
                    type: 'button',
                    onclick: (e) => {
                        Main.fetchExchangeAssetsToAdd().finally(m.redraw)
                    }
                }, 'Search'))
            ]),
            m('div.table-responsive', {style: 'max-height: 300px;'}, [
                m('table.table.table-hover', [
                    m('thead.thead-sticky.table-primary', m('tr', ['Ticker', 'ISIN', 'Exchange'].map(header =>
                        m('th', header)
                    ))),
                    m('tbody', data.map(obj =>
                        m('tr',
                            {
                                draggable: true,
                                ondragstart: (e) => {
                                    e.dataTransfer.setData('application/json', JSON.stringify({'exchange_asset': obj.id})); // Save the asset data
                                }
                            },
                            [
                                m('td', obj.ticker),
                                m('td', obj.asset_isin),
                                m('td', obj.exchange_mic),

                            ]
                        )
                    ))
                ])
            ])
        ])
    }
};


const AssetGroupsTable = {
    searchQuery: '',

    view: ({attrs}) => {
        const data = attrs.data;

        return  m('.d-flex.flex-column', [
            m('h5', 'Groups'),
            m('.input-group.mb-2', [
                m('input.form-control', {
                    style: 'font-size: 0.8rem;',
                    type: 'text',
                    placeholder: 'Search',
                    oninput: e => {
                        AssetGroupsTable.searchQuery = e.target.value;
                    },
                    value: AssetGroupsTable.searchQuery
                }),
                m('.input-group-append', m('button.btn.btn-outline-secondary', {
                    style: 'font-size: 0.8rem;',
                    type: 'button',
                    onclick: () => {
                        Main.fetchGroupsToAdd().finally(m.redraw)
                    }
                }, 'Search'))
            ]),
            m('div.table-responsive', {style: 'max-height: 300px;'}, [
                m('table.table.table-hover', [
                    m('thead.thead-sticky.table-primary', m('tr', ['Group name', 'Num assets'].map(header =>
                        m('th', header)
                    ))),
                    m('tbody', data.map(obj =>
                        m('tr',
                            {
                                draggable: true,
                                ondragstart: (e) => {
                                    e.dataTransfer.setData('application/json', JSON.stringify({'child_exchange_asset_group': obj.id})); // Save the group data
                                }
                            },
                            [
                                m('td', obj.name),
                                m('td', obj.num_assets),
                            ]
                        )
                    ))
                ])
            ])
        ])
    }
};


const FinalAssetsSetTable = {
    searchQuery: '',
    view: (vnode) => {
        const data = vnode.attrs.data;

        return  m('.d-flex.flex-column', [
            m('h5', 'Result'),
            m('.input-group.mb-2', [
                m('input.form-control', {
                    style: 'font-size: 0.8rem;',
                    type: 'text',
                    placeholder: 'Search',
                    oninput: e => {
                        FinalAssetsSetTable.searchQuery = e.target.value;
                    },
                    value: FinalAssetsSetTable.searchQuery
                }),
                m('.input-group-append', m('button.btn.btn-outline-secondary', {
                    style: 'font-size: 0.8rem;',
                    type: 'button',
                    onclick: () => {
                        Main.fetchFinalAssetsSet().finally(m.redraw)
                    }
                }, 'Search'))
            ]),
            m('div.table-responsive', {style: 'max-height: 700;'}, [
                m('table.table.table-hover', [
                    m('thead.thead-sticky.table-primary', [
                        m('tr', [
                            m('th', 'Ticker'),
                            m('th', 'ISIN'),
                            m('th', 'MIC'),
                            m('th', 'Start Period'),
                            m('th', 'End Period')
                        ])
                    ]),
                    m('tbody',
                        data.map(asset =>
                            asset.periods.map((period, index) => m('tr', [
                                m('td', index === 0 && asset.exchange_asset.ticker),
                                m('td', index === 0 && asset.exchange_asset.asset_isin),
                                m('td', index === 0 && asset.exchange_asset.exchange_mic),
                                m('td', period[0] || '-'),
                                m('td', period[1] || '-')
                            ]))
                        )
                    )
                ])
            ])
        ])
    }
};

const LoadingSpinner = {
    view: () => {
        return m('div', {
            class: 'spinner-border text-primary',
            role: 'status',

            style: 'position: fixed; top: 50%; left: 50%; width: 4rem; height: 4rem; z-index: 9999;'
        }, [
            m('span', {class: 'sr-only'},)
        ])
    }
};

const Main = {
    state: {
        groupsAll: [],
        selectedGroup: '',
        exchangeAssetsExisting: [],
        groupsExisting: [],
        exchangeAssetsToAdd: [],
        groupsToAdd: [],
        finalAssetsSet: [],
        loading: false,
    },
    setLoading: (value) => {
        Main.state.loading = value;
        m.redraw();
    },
    fetchGroups: () => {
        Main.setLoading(true);

        return fetch('/api/exchange-asset-group/')
            .then(response => response.json())
            .then(data => {
                Main.state.groupsAll = data;
                Main.state.loading = false;
            });
    },
    fetchExistingExchangeAssets: () => {
        if (Main.state.selectedGroup) {
            let url = `/api/group-exchange-asset/?exchange_asset_group=${Main.state.selectedGroup}`;
            if (ExchangeAssetsInGroupTable.searchQuery) {
                url += `&search=${ExchangeAssetsInGroupTable.searchQuery}`;
            }
            return fetch(url)
                .then(response => response.json())
                .then(data => {
                    Main.state.exchangeAssetsExisting = data;
                });
        }
    },
    fetchGroupsExisting: () => {
        if (Main.state.selectedGroup) {
            let url = `/api/group-exchange-asset-group/?parent_exchange_asset_group=${Main.state.selectedGroup}`;
            if (AssetGroupsInGroupTable.searchQuery) {
                url += `&search=${AssetGroupsInGroupTable.searchQuery}`;
            }

            return fetch(url)
                .then(response => response.json())
                .then(data => {
                    Main.state.groupsExisting = data;
                });
        }
    },
    fetchExchangeAssetsToAdd: () => {
        if (Main.state.selectedGroup) {
            let url = `/api/exchange-assets/?to_add_to_group=${Main.state.selectedGroup}`;
            if (ExchangeAssetsTable.searchQuery) {
                url += `&search=${ExchangeAssetsTable.searchQuery}`;
            }

            return fetch(url)
                .then(response => response.json())
                .then(data => {
                    Main.state.exchangeAssetsToAdd = data;
                });
        }
    },
    fetchGroupsToAdd: () => {
        if (Main.state.selectedGroup) {
            let url = `/api/exchange-asset-group/?to_add_to_group=${Main.state.selectedGroup}`;
            if (AssetGroupsTable.searchQuery) {
                url += `&search=${AssetGroupsTable.searchQuery}`;
            }
            return fetch(url)
                .then(response => response.json())
                .then(data => {
                    Main.state.groupsToAdd = data;
                });
        }
    },
    fetchFinalAssetsSet: () => {
        if (Main.state.selectedGroup) {
            let url = `/api/exchange-asset-group/${Main.state.selectedGroup}/?include_exchange_assets_result_list`;
            if (FinalAssetsSetTable.searchQuery) {
                url += `&search=${FinalAssetsSetTable.searchQuery}`;
            }
            return fetch(url)
                .then(response => response.json())
                .then(data => {
                    Main.state.finalAssetsSet = data.exchange_assets || [];
                });
        }
    },
    addGroupExchangeAsset: (data) => {
        Main.state.loading = true;

        return fetch('/api/group-exchange-asset/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                    'exchange_asset_group': Main.state.selectedGroup,
                    ...data,
                }
            )
        })
            .then(() => {
                    Promise.all([
                        Main.fetchExistingExchangeAssets(),
                        Main.fetchExchangeAssetsToAdd(),
                        Main.fetchFinalAssetsSet(),
                    ]).then(() => {
                        Main.state.loading = false;
                    }).finally(() => m.redraw())
                }
            );
    },
    patchGroupExchangeAsset: ({id, data}) => {
        Main.state.loading = true;
        return fetch(`/api/group-exchange-asset/${id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(() => {
                    Promise.all([
                        Main.fetchExistingExchangeAssets(),
                        Main.fetchExchangeAssetsToAdd(),
                        Main.fetchFinalAssetsSet(),
                    ]).then(() => {
                        Main.state.loading = false;
                    }).finally(() => m.redraw())
                }
            );
    },
    deleteGroupExchangeAsset: id => {
        Main.state.loading = true;
        return fetch(`/api/group-exchange-asset/${id}/`, {
            method: 'DELETE'
        })
            .then(() => {
                    Promise.all([
                        Main.fetchExistingExchangeAssets(),
                        Main.fetchExchangeAssetsToAdd(),
                        Main.fetchFinalAssetsSet(),
                    ]).then(() => {
                        Main.state.loading = false;
                    }).finally(() => m.redraw())
                }
            );
    },
    addGroupExchangeAssetGroup: (data) => {
        Main.state.loading = true;

        return fetch('/api/group-exchange-asset-group/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'parent_exchange_asset_group': Main.state.selectedGroup,
                ...data
            })
        })
            .then(() => {
                Promise.all([
                    Main.fetchGroupsExisting(),
                    Main.fetchGroupsToAdd(),
                    Main.fetchFinalAssetsSet(),
                ]).then(() => {
                    Main.state.loading = false;
                }).finally(() => m.redraw())
            });
    },
    patchGroupExchangeAssetGroup: ({id, data}) => {
        Main.state.loading = true;

        return fetch(`/api/group-exchange-asset-group/${id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(() => {
                    Promise.all([
                        Main.fetchGroupsExisting(),
                        Main.fetchGroupsToAdd(),
                        Main.fetchFinalAssetsSet(),
                    ]).then(() => {
                        Main.state.loading = false;
                    }).finally(() => m.redraw())
                }
            );
    },
    deleteGroupExchangeAssetGroup: id => {
        Main.state.loading = true;

        return fetch(`/api/group-exchange-asset-group/${id}/`, {
            method: 'DELETE'
        })
            .then(() => {
                    Promise.all([
                        Main.fetchGroupsExisting(),
                        Main.fetchGroupsToAdd(),
                        Main.fetchFinalAssetsSet(),
                    ]).then(() => {
                        Main.state.loading = false;
                    }).finally(() => m.redraw())
                }
            );
    },
    oninit: () => {
        Main.fetchGroups().finally(() => m.redraw());
    },
    view: () => {
        return m('div', {
            style: 'font-size: 0.8rem; margin: 20px'
        }, [
            m('h1', 'Asset group editing'),
            Main.state.loading && m(LoadingSpinner),
            m('div.form-group', [
                m('select.form-control', {
                    style: 'width: 300px',
                    value: Main.state.selectedGroup,
                    onchange: (e) => {
                        Main.state.selectedGroup = e.target.value;
                        Main.state.loading = true;
                        Promise.all([
                            Main.fetchExistingExchangeAssets(),
                            Main.fetchGroupsExisting(),
                            Main.fetchExchangeAssetsToAdd(),
                            Main.fetchGroupsToAdd(),
                            Main.fetchFinalAssetsSet()
                        ]).then(() => {
                            Main.state.loading = false;
                            m.redraw();
                        }).catch(error => {
                            console.error("Error fetching data: ", error);
                            Main.state.loading = false;
                            m.redraw();
                        });

                    }
                }, [
                    Main.state.selectedGroup === '' ? m('option', {value: ''}, 'Select a group') : null,
                    Main.state.groupsAll.map(group =>
                        m('option', {value: group.id}, group.name)
                    )
                ])
            ]),
            Main.state.selectedGroup && m('.row.mt-4', [
                m('', {
                    style: 'width: 35%'
                }, [
                    m(FinalAssetsSetTable, {data: Main.state.finalAssetsSet})
                ]),
                m('', {
                    style: 'width: 40%'
                }, [
                    m(ExchangeAssetsInGroupTable, {data: Main.state.exchangeAssetsExisting}),
                    m('.mt-3', m(AssetGroupsInGroupTable, {data: Main.state.groupsExisting}),)
                ]),
                m('', {
                    style: 'width: 25%'
                }, [
                    m(ExchangeAssetsTable, {data: Main.state.exchangeAssetsToAdd}),
                    m('.mt-3', m(AssetGroupsTable, {data: Main.state.groupsToAdd}))
                ])
            ])
        ]);
    }
};

m.route(
    root,
    "/",
    {
        "/": Main,
    }
)