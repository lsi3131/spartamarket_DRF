import {Link} from "react-router-dom";

export default function EmptyPage() {
    return (
        <>
            <h2>
                <Link to="/">잘못된 접근입니다.</Link>
            </h2>
        </>
    );
}