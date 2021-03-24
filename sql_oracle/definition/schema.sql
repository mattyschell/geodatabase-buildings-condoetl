declare
    psql varchar2(4000);
begin
    --anonymous pl/sql so we can call from cx_sde in test setup
    --otherwise this should be a script
    psql := 'create table condo ( '
         || '   condo_base_bbl      number(10,0) '
         || '  ,condo_billing_bbl   number(10,0) '
         || '  ,primary key (condo_base_bbl, condo_billing_bbl)'
         || ')';
    execute immediate psql;
    psql := 'create table condo_load ( '
         || '    condo_base_bbl      number(10,0) '
         || '   ,condo_billing_bbl   number(10,0) '
         || ')';
    execute immediate psql;
    psql := 'create table pluto_load ( '
         || '    bbl                 number(10,0) '
         || ')';
    execute immediate psql;
end; 
