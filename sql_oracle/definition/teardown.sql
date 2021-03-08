begin
    begin
        execute immediate 'drop table condo_load';
    exception
        when others then null;
    end;
    begin
        execute immediate 'drop table condo';
    exception
        when others then null;
    end;
end;